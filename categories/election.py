import discord
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta
from replit import db

from categories import database

president_role = 1279490327622713374
border_control = 1279500094370086943
citizenship_role = 1279494926912196668
president_channel = 1280663755088330814
v_president_role = 1279560073462419457
candidates_role = 1281395892284297277
questions = 1282425505450164336

class Election(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="startElection")
    async def startElection(self, ctx):
        isPresident = discord.utils.get(ctx.author.roles, id=president_role)
        if (not isPresident):
            await ctx.send(f"{ctx.author.mention}, you do not have permission to do this.")
            return
            
        db["electionActive"] = True
        db["votes"] = {}
        channel = self.bot.getChannel(president_channel)
        await channel.send("Election has begun!")
        
    @commands.command(name="endElection")
    async def endElection(self, ctx):
        isPresident = discord.utils.get(ctx.author.roles, id=president_role)
        if (not isPresident):
            await ctx.send(f"{ctx.author.mention}, you do not have permission to do this.")
            return
            
        db["electionActive"] = False
        channel = self.bot.getChannel(president_channel)
        await channel.send("Election has ended!")

    @commands.command(name="askQuestion")
    async def askQuestion(self, ctx, question: str = ""):
        role = ctx.guild.get_role(president_role)
        role2 = ctx.guild.get_role(candidates_role)
        role3 = ctx.guild.get_role(v_president_role)
        
        if (question == " "):
            await ctx.send(f"{ctx.author.mention}, you need to put your question after the command. For example, `>askQuestion will you give me admin powers?`")
        else:
            if (db["electionActive"]):
                if not question.endswith("?"):
                    question += "?"
                    
                channel = self.bot.getChannel(questions)
                await channel.send(f"{role.mention} {role2.mention} {role3.mention}, {ctx.author.name} has asked: {question}")
            else:
                await ctx.send(f"{ctx.author.mention}, there is no election right now.")

    @commands.command(name="vote")
    async def vote(self, ctx, party: str = " "):
        if (party == " "):
            await ctx.send(f"{ctx.author.mention}, type a political party after the command.")
            return
            
        if (db["electionActive"]):
            await ctx.send(f"{ctx.author.mention}, who are you voting for?")
        else:
            await ctx.send(f"{ctx.author.mention}, the election has ended. You can't vote anymore.")

async def setup(bot):
    await bot.add_cog(Election(bot))