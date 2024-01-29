import discord
from discord import app_commands
from discord.ext import commands

# ...
class Utility(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    class ScheduleGroup(app_commands.Group):
        pass
    schedule = ScheduleGroup(name="schedule", description="A group of commands used to manage schedules.")

    @schedule.command(description="Ask the bot to start the process to create a new schedule for you.")
    async def create(self, interaction:discord.Interaction):

        await interaction.response.send_message(f"`@{interaction.user.name} wants to make a new schedule.`")

    @schedule.command(description="Ask the bot to print out your schedule.")
    async def view(self, interaction:discord.Interaction):

        await interaction.response.send_message(f"`@{interaction.user.name}'s Schedule`")
        
async def setup(bot):
    
    await bot.add_cog(Utility(bot), guilds=[discord.Object(id=1165738081945653369)])