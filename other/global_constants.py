import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from mistralai import Mistral

from classes.game import Game

load_dotenv(dotenv_path="./sensitive.env", verbose=True, override=True)

BOT_TOKEN: str = os.environ['BOT_TOKEN']
BOT_ID: int = int(os.environ['BOT_ID'])
GAME_CHANNEL = 1366773148070056028

bot = commands.Bot(command_prefix="sc!", intents=discord.Intents.all(), activity=discord.CustomActivity(name="help me"), help_command=None)

api_key: str = os.environ['MISTRAL_API_KEY']
model = "open-mistral-nemo"
client = Mistral(api_key=api_key)

games: dict[int, Game] = {}