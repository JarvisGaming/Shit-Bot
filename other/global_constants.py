import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(dotenv_path="./sensitive.env", verbose=True, override=True)

BOT_TOKEN: str = os.environ['BOT_TOKEN']
BOT_ID: int = int(os.environ['BOT_ID'])
GAME_CHANNEL = 1366773148070056028

bot = commands.Bot(command_prefix="sc!", intents=discord.Intents.all(), activity=discord.CustomActivity(name="help me"), help_command=None)