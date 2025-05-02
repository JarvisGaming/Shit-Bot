import asyncio
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from other.global_constants import *


class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="start_game", description="Start the game!")
    async def profile(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"How To Play", colour=discord.Colour.blurple())
        text = """
        Given a scenario, your goal is to try to be the most \"compassionate\" and \"caring\" person you can possibly be.
        
        But, you will be facing against another chatbot, who will try to outdo you.
        
        Anything is fair game! (As long as it makes you look good, that is.)
        
        Do you have what it takes to one-up the AI?
        """
        embed.add_field(name='', value=text)
        
        await interaction.response.send_message(embed=embed)
        await asyncio.sleep(5)
        await interaction.followup.send("asdasdasd")
        

async def setup(bot: commands.Bot):
    await bot.add_cog(GameCog(bot))