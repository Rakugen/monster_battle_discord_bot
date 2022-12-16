import discord
import os
from discord.ext import commands

import game
from game import Player, run

TOKEN = os.getenv('BOT_TOKEN')
GUILD = os.getenv('GUILD_NAME')
INTENTS = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=INTENTS)

# BOT COMMANDS
# TODO: Start Game Command
@bot.command(name='game', help="Start Mon Battle Game.")
async def get_ascendant(ctx):
    # await ctx.send(response)
    pass


# TODO: Show Players Command
@bot.command(name='players', help="Show players.")
async def show_players(ctx):

    pass

# game.run()

# bot.run(TOKEN)
