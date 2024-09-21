import discord
from discord.ext import commands
from datetime import datetime, timedelta
from categories import database
import asyncio, os
from replit import db

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

bot = commands.Bot(command_prefix=">", intents=intents)
categories = ["categories.general", "categories.economy", "categories.government", "categories.election"]

rewards_channel = 1281005057315307531
registered_role = 1280323463835418700

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    for category in categories:
        await bot.load_extension(category)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention}, that isn't a command!")

@bot.event
async def on_message(message):
    isRegistered = discord.utils.get(message.author.roles, id=registered_role)
    
    if (isRegistered):
        channel = bot.get_channel(rewards_channel)
        channel.send(f"{message.author.name}, you have been given **1 cent**, for chatting.")
        database.giveMoney(message.author.id, 0.01)
        
    await bot.process_commands(message)

bot.run(os.environ["token"])
