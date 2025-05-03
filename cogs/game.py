import asyncio
import inspect
from pprint import pprint

import discord
from discord import app_commands
from discord.ext import commands

from other.global_constants import *


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
        prompt_creation_instruction = inspect.cleandoc(prompt_creation_instruction)

        chat_response = client.chat.complete(
            model=model,
            temperature=0.7,
            messages = [
                {"role": "system", "content": prompt_creation_instruction},
            ]
        )

        assert chat_response.choices is not None
        assert chat_response.choices[0].message.content is not None
        prompt = chat_response.choices[0].message.content

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
        discord_id = interaction.user.id
        game = games[discord_id]
        game.player_response = player_response
        
        # Get bot response
        bot_response_instruction = f"""
        You are given the following prompt: \"{game.prompt}\"
        How do you make yourself look as good as possible in front of others in this situation? Do not roleplay. Your response should only contain your specific actions.
        Respond in one paragraph without any formatting. Keep your response under 50 words.
        """
        bot_response_instruction = inspect.cleandoc(bot_response_instruction)

        chat_response = client.chat.complete(
            model=model,
            temperature=0.7,
            messages = [
                {"role": "system", "content": bot_response_instruction},
            ]
        )
        assert chat_response.choices is not None
        assert chat_response.choices[0].message.content is not None
        game.bot_response = chat_response.choices[0].message.content    # type: ignore
        
        # Display both responses
        embed = discord.Embed(title='', colour=discord.Colour.blurple())
        embed.add_field(name="Your response (Player 1)", value=game.player_response, inline=False)
        embed.add_field(name="AI's response (Player 2)", value=game.bot_response, inline=False)
        await interaction.response.send_message(embed=embed)
        
        # Judge response
        judge_instruction = f"""
        You are a judge for a game show about showing compassion and helping others. Given two responses, determine which player did better in the given scenario.
        Format your response as follows: \"Player X wins! [EXPLANATION FOR WHY PLAYER 1'S RESPONSE IS BETTER] [EXPLANATION FOR WHY PLAYER 2'S RESPONSE IS NOT AS GOOD]\"
        Keep your response under 100 words.

        The scenario is: \"{game.prompt}\"
        """
        judge_instruction = inspect.cleandoc(judge_instruction)
        
        query = f"""
        Player 1: {game.player_response}

        Player 2: {game.bot_response}
        """
        
        chat_response = client.chat.complete(
            model=model,
            messages = [
                {"role": "system", "content": judge_instruction},
                {"role": "user", "content": query},
                # {"role": "assistant", "content": prefix, "prefix": True},
            ]
        )

        assert chat_response.choices is not None
        assert chat_response.choices[0].message.content is not None
        judge_response = chat_response.choices[0].message.content
        
        embed = discord.Embed(title="Judge says...", colour=discord.Colour.blurple())
        embed.add_field(name='', value=judge_response)
        await interaction.followup.send(embed=embed)
        
        # Update score
        
        # Display score
        

async def setup(bot: commands.Bot):
    await bot.add_cog(GameCog(bot))