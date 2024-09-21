import discord
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta
from replit import db

from categories import database

president_role = 1279490327622713374
border_control = 1279500094370086943
citizenship_role = 1279494926912196668

class Government(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clearMemory")
    async def clearMemory(self, ctx):
        isPresident = discord.utils.get(ctx.author.roles, id=president_role)
        if (isPresident):
            for key in db.keys():
                del db[key]

            await ctx.send(f"{ctx.author.mention}, the database has been cleared.")
        else:
            await ctx.send(f"{ctx.author.mention}, you do not have permission to do this.")

    @commands.command(name="removeCitizenship")
    async def removeCitizenship(self, ctx, member: discord.Member):
        isPresident = discord.utils.get(ctx.author.roles, id=president_role)
        role = discord.utils.get(ctx.guild.roles, id=citizenship_role)
        role2 = discord.utils.get(ctx.guild.roles, id=border_control)

        if (isPresident):
            if role in member.roles or role2 in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"Removed citzenship from {member.mention}.")
            else:
                await ctx.send(f"{member.mention} doesn't have citizenship.")
        else:
            await ctx.send(f"{ctx.author.mention}, you do not have government permission to do this.")

async def setup(bot):
    await bot.add_cog(Government(bot))