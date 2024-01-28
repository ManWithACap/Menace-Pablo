import discord, os, dotenv, ctypes
from discord.ext import commands
from colors import Colors

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
    print(f"\n{Colors.GREEN}\nMenace, reporting for duty.\n{Colors.RESET}\n")

# on_message Event Listener
@bot.event
async def on_message(message):

    # If the bot is DM'd "ping", return "pong".
    if message.content == "ping":

        await message.channel.send("pong")

# Turn the bot on.
bot.run(token)