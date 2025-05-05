import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from together import Together

from classes.game import Game

load_dotenv(dotenv_path="./sensitive.env", verbose=True, override=True)

BOT_TOKEN: str = os.environ['BOT_TOKEN']
GAME_CHANNEL = 1366773148070056028

bot = commands.Bot(command_prefix="one!", intents=discord.Intents.all(), activity=discord.CustomActivity(name="Run /start_game to start!"), help_command=None)

api_key: str = os.environ['TOGETHER_API_KEY']
model = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"
client = Together()

games: dict[int, Game] = {}