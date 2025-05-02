import datetime
import os

import dotenv
from discord import app_commands
from discord.ext import tasks

from other.global_constants import *

async def send_in_all_channels(message: str):
    """Sends <message> in all approved channels."""
    
    channel = bot.get_channel(GAME_CHANNEL)
    await channel.send(message)  # type: ignore