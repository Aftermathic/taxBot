import discord
from discord.ext import commands
from replit import db
import math

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="echo")
    async def echo(self, ctx, *, message: str = " "):
        if (message == " "):
            await ctx.send(f"{ctx.author.mention}, you gotta put something after the command for me to echo it. For example, `>echo Good morning!`")
            return
            
        await ctx.send(message)

    @commands.command(name="calculate")
    async def calculate(self, ctx, *, message: str = " "):
        if (message == " "):
            await ctx.send(f"{ctx.author.mention}, you gotta put some math after the command. For example, `>calculate 1 + 1`")
            return

        try:
            allowed_functions = {
                "sqrt": math.sqrt,
                "pow": math.pow,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "log": math.log,
                "__builtins__": None
            }

            result = eval(message, {"__builtins__": None}, allowed_functions)
            await ctx.send(f"The result of `{message}` is: {result}")
        except Exception as e:
            await ctx.send(f"{ctx.author.mention}, there was an error.")

async def setup(bot):
    await bot.add_cog(General(bot))