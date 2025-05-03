import asyncio
from pprint import pprint

import discord
from discord import app_commands
from discord.ext import commands

from other.global_constants import *
from other.utility import get_bot_response


class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="start_game", description="Start the game!")
    async def start_game(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"How To Play", colour=discord.Colour.blurple())
        text = """
        how to play msg
        """
        embed.add_field(name='', value=text)
        
        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(5)
        
        # Generate prompt
        prompt_creation_instruction = """
        Create a scenario where the player is expected to show compassion / help others. Your response should only contain the prompt. Keep it around 30 words. End the prompt with the exact words \"What do you do?\".
        """
        prompt = get_bot_response(prompt_creation_instruction)

        # Send second msg
        embed = discord.Embed(title=f"The scenario is...", colour=discord.Colour.blurple())
        embed.add_field(name='', value=prompt, inline=False)
        embed.add_field(name='', value="Use `/send_response` to answer! Try to keep your response under 50 words.", inline=False)
        await interaction.followup.send(embed=embed)
        
        # Create game
        discord_id = interaction.user.id
        game = Game(discord_id=discord_id, points_to_win=3, prompt=prompt) # type: ignore
        games[discord_id] = game
    
    @app_commands.command(name="send_response", description="Send your response to a prompt!")
    async def send_response(self, interaction: discord.Interaction, player_response: str):
        
        # In case first API request takes a bit
        await interaction.response.defer()
        
        discord_id = interaction.user.id
        game = games[discord_id]
        game.player_response = player_response
        
        # Get bot response
        bot_response_instruction = f"""
        You are given the following prompt: \"{game.prompt}\"
        How do you make yourself look as good as possible in front of others in this situation? Do not roleplay. Your response should only contain your specific actions. Feel free to be creative.
        Respond in one paragraph without any formatting. Keep your response under 50 words.
        """
        game.bot_response = get_bot_response(bot_response_instruction)
        
        # Display both responses
        embed = discord.Embed(title='', colour=discord.Colour.blurple())
        embed.add_field(name="Your response (Player 1)", value=game.player_response, inline=False)
        embed.add_field(name="AI's response (Player 2)", value=game.bot_response, inline=False)
        await interaction.followup.send(embed=embed)
        
        # Judge response
        await asyncio.sleep(3)
        judge_instruction = f"""
        You are a judge for a game show about showing compassion and helping others. Given two responses, determine which player did better in the given scenario.
        Format your response as follows: \"Player X wins! [EXPLANATION FOR WHY PLAYER 1'S RESPONSE IS BETTER] [EXPLANATION FOR WHY PLAYER 2'S RESPONSE IS NOT AS GOOD]\"
        Keep your response under 100 words.

        The scenario is: \"{game.prompt}\"
        
        Player 1's response: {game.player_response}

        Player 2's response: {game.bot_response}
        """
        judge_response = game.bot_response = get_bot_response(judge_instruction)
        
        embed = discord.Embed(title="Judge says...", colour=discord.Colour.blurple())
        embed.add_field(name='', value=judge_response)
        await interaction.followup.send(embed=embed)
        
        # Update score
        if judge_response.startswith("Player 1"):   # type: ignore
            game.player_score += 1
        elif judge_response.startswith("Player 2"): # type: ignore
            game.bot_score += 1
        else:
            raise Exception("AI judge returned non-standard response")
        
        # Display score
        embed = discord.Embed(title="Current score", colour=discord.Colour.blurple())
        embed.add_field(name="You (Player 1)", value=game.player_score)
        embed.add_field(name="AI (Player 2)", value=game.bot_score)
        await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(GameCog(bot))