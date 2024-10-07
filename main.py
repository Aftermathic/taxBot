import os
import discord
from discord.ext import commands
import database
from replit import db

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

# db.clear()
# above is to clear database, if you're not president

bot = commands.Bot(command_prefix=">", intents=intents, help_command=None)

def format_currency(amount):
    return "${:,.2f}".format(amount)

all_channels = {
    "rewards": 1292534768491171891,
    "payday": 1281055783118835722,
    "welcome": 1292285669158158376
}

all_roles = {
    "registered": 1280323463835418700,
    "citizen": 1292653837705936978,
    "border control": 1279500094370086943,
    "candidates": 1281395892284297277,
    "vice president": 1279560073462419457,
    "president": 1279490327622713374,

    # jobs, hopefully will be worked on soon
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
    if message.author.bot:
        return
        
    isCitizen = discord.utils.get(message.author.roles, id=all_roles["citizen"])
    if (isCitizen):
        channel = bot.get_channel(all_channels["rewards"])
        database.addToBalance(str(message.author.id), 0.05)
        await channel.send(f"{message.author.name}, you have been given **5¢**, for chatting.")

    await bot.process_commands(message)

@bot.command(help="See who's winning the election! (still in testing...)")
async def polls(ctx):
    polls = database.getVotes()
    if (polls == "None"):
        await ctx.send(f"{ctx.author.mention}, no one has voted yet.")
    else:
        candidates = []
        role = ctx.guild.get_role(all_roles["candidates"])
        for member in ctx.guild.members:
            if (role in member.roles):
                viceprezid = database.getRunningMate(str(member.id))

                if (viceprezid != "None"):
                    viceprez = ctx.guild.get_member(viceprezid)
                    candidates.append(f"**{member.name}** and **{viceprez.name}**")
                else:
                    viceprez = "None"
                    candidates.append(f"**{member.name}** and **{viceprez}**")
                
        for vote in polls:
            candidate_votes = {}

            for userid, candidate in polls.items():
                if candidate in candidate_votes:
                    candidate_votes[candidate] += 1
                else:
                    candidate_votes[candidate] = 1

            message = "**Current Poll Results:**\n"
            for candidate, count in candidate_votes.items():
                cand = candidates[candidate]
                message += f"{cand}: {count} votes\n"

            await ctx.send(message)
        
@bot.command(help="Vote for the next president. (still in testing...)")
async def vote(ctx, whichone: int = 99999):
    candidates = []
    role = ctx.guild.get_role(all_roles["candidates"])
    for member in ctx.guild.members:
        if (role in member.roles):
            viceprezid = database.getRunningMate(str(member.id))

            if (viceprezid != "None"):
                viceprez = ctx.guild.get_member(viceprezid)
                candidates.append([member.name, viceprez.name])
            else:
                viceprez = "None"
                candidates.append([member.name, viceprez])

    message = ""
    counter = 0
    for candidate in candidates:
        message += f"{counter}: **{candidate[0]}** and **{candidate[1]}**\n"            
        counter += 1
        
    try:
        vote = candidates[whichone]
    except:
        await ctx.send(f"{ctx.author.mention}, here are the candidates.\n\n{message}\n{ctx.author.mention}, you may have entered an invalid number. In order to vote, put the number after that command that corresponds to them. For example, `>vote 0`.")
    else:
        if (database.votes(ctx.author.id, whichone)):
            await ctx.send(f"{ctx.author.mention}, you voted for **{vote[0]}** and **{vote[1]}**!")
        else:
            await ctx.send(f"{ctx.author.mention}, you already voted. You can't change it.")   

@bot.command(help="Only if you won the primaries, you can use this command to choose your running mate. Don't use this command if you do not want to have a running mate.")
async def chooseRunningMate(ctx, user: discord.Member = None):
    role = ctx.guild.get_role(all_roles["candidates"])
    member = ctx.guild.get_member(ctx.author.id)
    if (user is None):
        if (role in member.roles):
            await ctx.send(f"{ctx.author.mention}, you have to ping your running mate after the command. Example: `>chooseRunningMate @aftermathic`")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not a candidate.")
    else:
        running_mateid = user.id
        database.setRunningMate(str(ctx.author.id), running_mateid)

        await ctx.send(f"You have chosen {user.mention} as your running mate.")

@bot.command()
async def help(ctx):
    commands_message = ""

    for command in bot.commands:
        if command.name == "help":
            commands_message += f"**{command.name}** - *Shows this message.*\n"
        else:
            description = command.help if command.help else "No description available."
            commands_message += f"**{command.name}** - *{description}*\n"

    await ctx.send(f"{ctx.author.mention}, here are the available commands:\n\n{commands_message}")

@bot.command(help="Check how much money you got in your balance.")
async def checkBalance(ctx):
    await ctx.send(f"{ctx.author.mention}, you have **{format_currency(database.getBalance(str(ctx.author.id)))}** in your balance.")

@bot.command(help="Clear roles, debts, everyone's balance, everything. Only availible to the president.")
async def clearEverything(ctx):
    role = ctx.guild.get_role(all_roles["president"])
    member = ctx.guild.get_member(ctx.author.id)
    if (role in member.roles):
        database.clearDatabase()
        for user in ctx.guild.members:
            for role in all_roles:
                if (role in user.roles):
                    await user.remove_roles(role)
                
        await ctx.send(f"{ctx.author.mention}, Mr. President...\nIt has been done. In hopes of a new and better system...")
    else:
        await ctx.send(f"{ctx.author.mention}, you are not allowed to do that.")

@bot.command(help="Use this command to register to vote.")
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

@bot.command(help="Used by border control to allow immigrants into the country.")
async def giveCitizenship(ctx, user: discord.Member = None):        
    role = ctx.guild.get_role(all_roles["citizen"])
    member = ctx.guild.get_member(ctx.author.id)
    border_control = discord.utils.get(ctx.guild.roles, id=all_roles["border control"])
    
    if (user is None):
        if (border_control in member.roles):
            await ctx.send(f"{ctx.author.mention}, you must specify a user to give citizenship.")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not border control.")

        return

    if (border_control in member.roles):
        if (role in member.roles):
            await ctx.send(f"{ctx.author.mention}, they are already a citizen.")
            
        try:
            await user.add_roles(role)
        except :
            await ctx.send(f"{ctx.author.mention}, something went wrong. Try again another time.")
        else:
            await ctx.send(f"{ctx.author.mention}, {user.name} has been allowed in the country.")

            channel = bot.get_channel(all_channels["welcome"])
            await channel.send(f"{user.mention}, welcome to the country!\nYou will start with **$1,000** in your account. Use `>help` command to see all commands you can use!")
    else:
        await ctx.send(f"{ctx.author.mention}, you are not border control.")

bot.run(os.environ["token"])
