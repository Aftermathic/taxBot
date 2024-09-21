import discord
import asyncio
from discord.ext import commands
from datetime import datetime, timedelta
from replit import db

from categories import database

registered_role = 1280323463835418700

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="checkBalance")
    async def checkBalance(self, ctx):
        isRegistered = discord.utils.get(ctx.author.roles, id=registered_role)
        if (isRegistered):
            await ctx.send(f"{ctx.author.mention}, your balance is: **${database.getBalance(ctx.author.id):,}**")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not registered. Please register by typing `>register`")

    @commands.command(name="register")
    async def register(self, ctx):
        isRegistered = discord.utils.get(ctx.author.roles, id=registered_role)
        if (isRegistered):
            await ctx.send(f"{ctx.author.mention}, you're already registered.")
        else:
            try:
                await ctx.author.add_roles(registered_role)
            except:
                await ctx.send(f"{ctx.author.mention}, something went wrong. Try again another time.")
                return

            database.giveMoney(ctx.author.id, 500)
            database.createDueDates(ctx.author.id, True, False)
            await ctx.send(f"{ctx.author.mention}, you're now registered! You have been given $500 for your starting balance.")

    @commands.command(name="requestLoan")
    async def requestLoan(self, ctx, amount: int = 0):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
            
        isRegistered = discord.utils.get(ctx.author.roles, id=registered_role)
        currentBalance = database.getBalance(ctx.author.id)
        if (isRegistered):
            if (amount < 0):
                await ctx.send(f"{ctx.author.mention}, why would I request a negative amount of money from the bank?")
                return
            elif (amount == 0):
                await ctx.send(f"{ctx.author.mention}, there you go, ||**$0.00**||, you're welcome. Type how much you want to request after the command, with no commas or anything. Just the number, for example: `>requestLoan 1000`")
            else:
                if (amount >= currentBalance):
                    await ctx.send(f"{ctx.author.mention}, are you sure? If you lose all of this money, and don't get anything back from it, you will go bankrupt. Respond with yes or no.")
                    
                    try:
                        response = await self.bot.wait_for("message", timeout=10.0, check=check)
                    except asyncio.TimeoutError:
                        await ctx.send(f"{ctx.author.mention}, you took too long to respond!")
                    except:
                        await ctx.send(f"{ctx.author.mention}, something went wrong.")
                    else:
                        usersaid = response.content.lower()
                        if (usersaid == "yes"):
                            await ctx.send(f"{ctx.author.mention}, the loan has been sucessful. Be careful.")
                            database.giveMoney(ctx.author.id, amount)
                            database.createDueDates(ctx.author.id, False, True)
                        else:
                            await ctx.send(f"{ctx.author.mention}, the loan has been canceled.")

                    return
                        
                if (currentBalance >= 500):
                    await ctx.send(f"{ctx.author.mention}, seems you're in a tricky spot. Your loan has been approved. You will pay this back next week.")
                    database.createDueDates(ctx.author.id, False, True)
                    database.giveMoney(ctx.author.id, amount)
                else:
                    await ctx.send(f"{ctx.author.mention}, your loan has been approved. You will pay it off next week.")
                    database.createDueDates(ctx.author.id, False, True)
                    database.giveMoney(ctx.author.id, amount)
        else:
            await ctx.send(f"{ctx.author.mention}, please register first.")

async def setup(bot):
    await bot.add_cog(Economy(bot))