import discord
from discord import app_commands
from discord.ext import commands

from other.global_constants import *
from other.utility import get_bot_response


class MiscCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ask_bot", description="Ask the AI anything!")
    async def ask_bot(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        bot_response = get_bot_response(query)
        
        # Sometimes the bot likes going off the rails
        MESSAGE_LENGTH_LIMIT = 2000
        if len(bot_response) > MESSAGE_LENGTH_LIMIT:
            bot_response = bot_response[:1996]
            bot_response += "..."
            
        await interaction.followup.send(content=bot_response)

async def setup(bot: commands.Bot):
    await bot.add_cog(MiscCog(bot))