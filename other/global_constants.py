import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from together import Together

from classes.game import Game

# from mistralai import Mistral

load_dotenv(dotenv_path="./sensitive.env", verbose=True, override=True)

BOT_TOKEN: str = os.environ['BOT_TOKEN']
BOT_ID: int = int(os.environ['BOT_ID'])
GAME_CHANNEL = 1366773148070056028

bot = commands.Bot(command_prefix="one!", intents=discord.Intents.all(), activity=discord.CustomActivity(name="Run /start_game to start!"), help_command=None)

# api_key: str = os.environ['MISTRAL_API_KEY']
# model = "open-mistral-nemo"
# client = Mistral(api_key=api_key)

api_key: str = os.environ['TOGETHER_API_KEY']
model = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"
client = Together()

games: dict[int, Game] = {}