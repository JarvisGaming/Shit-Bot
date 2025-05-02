import os
import sys

import other.utility
from other.error_handling import *


@bot.event
async def setup_hook():
    """This is run once when the bot starts."""
    
    # await load_all_cogs()
    await bot.tree.sync()  # Syncs slash commands
    
async def load_all_cogs():
    """Load bot commands stored in the cogs folder."""

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
            except Exception as error:
                await other.utility.send_in_all_channels(f"**Failed to load {filename}: {error}**")
    
@bot.event
async def on_ready():
    """Runs after setup_hook()."""
    
    await other.utility.send_in_all_channels("Bot is now ready")

sys.stderr = open("./logs.log", "w")  # Redirect stderr to log file
bot.run(BOT_TOKEN)