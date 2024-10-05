import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

bot = commands.Bot(command_prefix=">", intents=intents, help_command=None)

all_channels = {
    "rewards": 1281005057315307531,
    "payday": 1281055783118835722
}

all_roles = {
    "registered": 1280323463835418700,
    "citizen": 1279494926912196668,
    "border control": 1279500094370086943,
    "candidates": 1281395892284297277,
    "vice president": 1279560073462419457,
    "president": 1279490327622713374,

    "army": 1280669829774315540
}

all_jobs = { # "job_name": [payout, role]   payout is every week
    "army": [490, all_roles["army"]]
}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention}, that isn't a command!")

@bot.event
async def on_message(message):
    isRegistered = discord.utils.get(message.author.roles, id=all_roles["registered"])
    
    await bot.process_commands(message)
    
    if (isRegistered):
        channel = bot.get_channel(all_channels["rewards"])
        await channel.send(f"{message.author.name}, you have been given **5¢**, for chatting.")

@bot.command()
async def help(ctx):
    commands_list = [command.name for command in bot.commands]
    commands_message = ""

    for command in commands_list:
        if (command == "help"):
            commands_message += f"**{command}** - shows this message.\n"
        else:
            commands_message += f"**{command}**\n"
            
    await ctx.send(f"{ctx.author.mention}, all of the commands that I have are below.\n{commands_message}")

@bot.command()
async def registerToVote(ctx):
    member = ctx.guild.get_member(ctx.author.id)
    role = ctx.guild.get_role(all_roles["registered"])

    if (role in member.roles):
        await ctx.send(f"{ctx.author.mention}, you are already registered to vote.")
        return

    try:
        await member.add_roles(role)
    except:
        await ctx.send(f"{ctx.author.mention}, something went wrong. Try again another time.")
    else:
        await ctx.send(f"{ctx.author.mention}, you are now registered to vote! However if you don't vote on elections, you will get taxed.")

@bot.command()
async def giveCitizenship(ctx, member: discord.Member):
    role = ctx.guild.get_role(all_roles["citizen"])
    member = ctx.guild.get_member(ctx.author.id)
    border_control = discord.utils.get(ctx.guild.roles, id=all_roles["border control"])

    if (border_control in member.roles):
        try:
            await member.add_roles(role)
        except:
            await ctx.send(f"{ctx.author.mention}, something went wrong. Try again another time.")
        else:
            await ctx.send(f"{ctx.author.mention}, {member.name} has been allowed in the country.")
    else:
        await ctx.send(f"{ctx.author.mention}, you are not border control.")

bot.run(os.environ["token"])
