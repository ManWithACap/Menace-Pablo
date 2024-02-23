import discord, os, dotenv, ctypes, asyncio
import ansi.colour as Colors
from discord.ext import commands

# Set console mode to make sure the escape sequences are processed correctly.
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# Load in the local .env file.
dotenv.load_dotenv()

# Global Variables
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="m.", intents=intents)
token = os.getenv("API_TOKEN")

# on_ready Event Listener
@bot.event
async def on_ready():

    # Bot Ready Message
    print(f"\n{Colors.fg.green}\nMenace, reporting for duty.\n{Colors.fx.reset}")

    await bot.wait_until_ready()
    fmt = await bot.tree.sync(guild=bot.get_guild(675390519714775060))
    print(f"Synced {len(fmt)} commands.")

# Tree-clearing Command
@bot.command()
async def clear(ctx):

    if ctx.author.guild_permissions.administrator:

        bot.tree.clear_commands(guild=ctx.guild)
        await ctx.send("Cleared the existing commands.")

    else:

        await ctx.send("You do not have admin privilages.\nTherefore, you are not authorized to run this command.\nHow do you even know about this one? 🤔")

# Async Function for Extension Loading
async def load():

    for cog in os.listdir("./cogs"):

        if cog != "__pycache__":

            try:

                await bot.load_extension(f"cogs.{cog[:-3]}")
                print("success: " + cog[:-3])

            except Exception as e:

                print(f"failure: {e}")

# Run the function.
asyncio.run(load())

# Turn the bot on.
bot.run(token)