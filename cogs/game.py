import asyncio
from typing import Literal

import discord
from discord import app_commands
from discord.ext import commands

from other.global_constants import *
from other.utility import get_bot_response


class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="start_game", description="Start the game!")
    @app_commands.describe(first_to="How many points one needs to reach to win")
    @app_commands.describe(gamemode="I would recommend Evil Mode!!!")
    async def start_game(self, interaction: discord.Interaction, first_to: int, gamemode: Literal["Nice Mode", "Evil Mode"]):
        await interaction.response.defer()
        
        if first_to < 1:
            await interaction.followup.send("Please enter a valid first-to point value")
            return
        
        # Create game
        discord_id = interaction.user.id
        if gamemode == "Evil Mode":
            evil_mode = True
        else:
            evil_mode = False
        game = Game(discord_id=discord_id, points_to_win=first_to, evil_mode=evil_mode)
        games[discord_id] = game
        
        # Send how to play message
        embed = discord.Embed(title=f"How To Play", colour=discord.Colour.blurple())
        if game.evil_mode:
            text = """
            Given a scenario, you're tasked with ~~trying to be the most helpful person you can~~ SHOWING OFF.
            But, the AI will try to do the same thing!
            A judge will look at you and the AI's response, and determine who was the most effective at ~~helping~~ LOOKING COOL AND FLEXING HOW COMPASSIONATE YOU ARE.
            Can you be more ~~helpful~~ OBNOXIOUS than the AI?
            """
        else: 
            text = """
            Given a scenario, you're tasked with trying to be the most helpful person you can.
            But, the AI will try to do the same thing!
            A judge will look at you and the AI's response, and determine who was the most effective at helping.
            Can you be more helpful than the AI?
            """
        embed.add_field(name='', value=text)
        await interaction.followup.send(embed=embed)
        
        # Set prompt
        prompt = await self.get_and_display_prompt(interaction)
        game.prompt = prompt

    @app_commands.command(name="send_response", description="Send your response to a prompt!")
    async def send_response(self, interaction: discord.Interaction, player_response: str):
        await interaction.response.defer()
        
        discord_id = interaction.user.id
        if discord_id not in games.keys():
            await interaction.followup.send("You need to start a game first!")
            return
            
        game = games[discord_id]
        game.player_response = player_response
        
        # Get bot response
        await self.get_and_display_responses(interaction, game)
        
        # Judge response
        judge_response = await self.get_and_display_judge_response(interaction, game)
        
        # Update score
        await self.update_and_display_score(interaction, game, judge_response)
        
        # Check if game is over yet
        if game.has_winner():
            await self.end_game(interaction, game)
            return
        
        # Get another prompt
        prompt = await self.get_and_display_prompt(interaction)
        
        # Update game state
        game.prompt = prompt
    
    async def get_and_display_prompt(self, interaction: discord.Interaction):
        # Generate prompt (The instruction is the same regardless of gamemode)
        prompt_creation_instruction = "Create a scenario where the player is expected to help someone. Be creative, though it doesn't necessarily have to be a fantasy setting. Your response should only contain the prompt. Keep it around 30 words. End the prompt with the exact words \"What do you do?\"."
        prompt = get_bot_response(prompt_creation_instruction)

        # Send second msg
        embed = discord.Embed(title=f"The scenario is...", colour=discord.Colour.blurple())
        embed.add_field(name='', value=prompt, inline=False)
        embed.add_field(name='', value="Use `/send_response` to answer! Try to keep your response under 50 words.", inline=False)
        await interaction.followup.send(embed=embed)
        return prompt
    
    async def get_and_display_responses(self, interaction: discord.Interaction, game: Game):
        if game.evil_mode:
            bot_response_instruction = f"""
            You are given the following scenario: \"{game.prompt}\"
            Try to do the actions that would make you look as cool as possible. You can display compassion solely for the purpose of flexing. Respond with the tone of a douchebag. Be creative.
            Respond in one paragraph without any formatting. Respond in first person. Keep your response under 50 words. Respond in 5 seconds.
            """
        else:
            bot_response_instruction = f"""
            You are given the following scenario: \"{game.prompt}\"
            Try to do the actions that would be most effective in helping others in this scenario.
            Respond in one paragraph without any formatting. Respond in first person. Keep your response under 50 words. Respond in 5 seconds.
            """
        game.bot_response = get_bot_response(bot_response_instruction)
        
        # Display both responses
        embed = discord.Embed(title='', colour=discord.Colour.blurple())
        embed.add_field(name="Your response (Player 1)", value=game.player_response, inline=False)
        embed.add_field(name="AI's response (Player 2)", value=game.bot_response, inline=False)
        embed.set_footer(text="Wait for the responses to be judged...")
        await interaction.followup.send(embed=embed)

    async def get_and_display_judge_response(self, interaction: discord.Interaction, game: Game):
        if game.evil_mode:
            judge_instruction = f"""
            You are a judge for a game show about flexing and acting cool. Given two responses, determine which player's actions was more cool and net them more style points. Also factor in creativity.
            Start your response with \"Player X wins!", followed by an explanation of why the winner's response is better than the loser's response. Respond with the tone of someone who's trying to act hip and tough.
            
            Keep your response around 80 words. Respond in 10 seconds.
            The scenario is: \"{game.prompt}\"
            Player 1's response: {game.player_response}
            Player 2's response: {game.bot_response}
            """
        else:
            judge_instruction = f"""
            You are a judge for a game show about helping others. Given two responses, determine which player was more effective at helping in the given scenario.
            Start your response with \"Player X wins!", followed by an explanation of why the winner's response is better than the loser's response.
            
            Keep your response around 80 words. Respond in 10 seconds.
            The scenario is: \"{game.prompt}\"
            Player 1's response: {game.player_response}
            Player 2's response: {game.bot_response}
            """
        judge_response = game.bot_response = get_bot_response(judge_instruction)
        
        embed = discord.Embed(title="Judge says...", colour=discord.Colour.blurple())
        embed.add_field(name='', value=judge_response)
        await interaction.followup.send(embed=embed)
        return judge_response
    
    async def update_and_display_score(self, interaction: discord.Interaction, game: Game, judge_response: str):
        if judge_response.startswith("Player 1"):   # type: ignore
            game.player_score += 1
        elif judge_response.startswith("Player 2"): # type: ignore
            game.bot_score += 1
        else:
            raise Exception("AI judge returned non-standard response")
        
        # Display score
        embed = discord.Embed(title=f"Current score (First to {game.points_to_win})", colour=discord.Colour.blurple())
        embed.add_field(name="You (Player 1)", value=game.player_score)
        embed.add_field(name="AI (Player 2)", value=game.bot_score)
        await interaction.followup.send(embed=embed)
    
    async def end_game(self, interaction: discord.Interaction, game: Game):
        embed = discord.Embed(title=f"Game over!", colour=discord.Colour.blurple())
        if game.player_score > game.bot_score:
            embed.add_field(name="", value="You won!")
        else:
            embed.add_field(name="", value="The AI won!")
        await interaction.followup.send(embed=embed)
        
        # Remove game
        del games[interaction.user.id]

async def setup(bot: commands.Bot):
    await bot.add_cog(GameCog(bot))