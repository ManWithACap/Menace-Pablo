import discord
from discord.ext import commands
from discord import app_commands

# A Class of Useless Commands That Don't Do Anything Useful
class Useless(commands.Cog):
    
    def __init__(self, bot):

        self.bot = bot

    # Hello Command
    @commands.command()
    async def hello(self, ctx):
        
        await ctx.send("Hello!")

    # Ping Command
    @commands.command()
    async def ping(self, ctx):
        
        await ctx.send("pong")
    
    # Pong Command
    @commands.command()
    async def pong(self, ctx):
        
        await ctx.send("ping")

# Setup Function
async def setup(bot):
    
    await bot.add_cog(Useless(bot), guilds=[discord.Object(id=1165738081945653369)])