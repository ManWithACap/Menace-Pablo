import discord, os, typing, aiofiles, json, re, validators
from ast import literal_eval
import datetime as dt
from discord import app_commands
from discord.ext import commands

changelog = {}
with open("data/changelog.json", "r") as file:
                
    changelog = json.loads(file.read())
    file.close()
botVersion = changelog["version"]

# These commands are used for various functions that are menat to be more like tools or stations.
class Utility(commands.Cog):

    @app_commands.command()
    async def help(self, interaction:discord.Interaction, command:typing.Literal["all", "schedule"]):

        match command:

            case "all":

                await interaction.response.send_message("Not implemented yet.")

            case "schedule":

                embed = discord.Embed(title="Schedule", description="A group of commands used to manage schedules.", timestamp=dt.datetime.now(), color=0x2a783f)
                embed.set_author(name="Menace", icon_url="https://cdn.discordapp.com/avatars/1044144223018041344/358cd1a4add10228c4962dd130a7bfd7?size=1024")
                embed.add_field(name="\"view\"", value="`member`: the user who's schedule you want to view.")
                embed.add_field(name="\"create\"", value="This has a number of fields but each field is self explanitory.")
                embed.add_field(name="\"edit\"", value="`choice`: \nFor \"Hex Code Color\", make sure to use something like [Google's color picker](https://g.co/kgs/a5zGFqo).\nIf you want to get your profile picture URL, use something like [Toolscord](https://toolscord.com) to grab your discord URL. Only image URLs will work for your icon.")

                await interaction.response.send_message(embed=embed)
    
    @app_commands.command()
    async def whatsnew(self, interaction:discord.Interaction):

        embed = discord.Embed(title=botVersion, description="*Here's a look at the most recent update for the bot's features:*", timestamp=dt.datetime.now(), color=0x2a783f)
        embed.set_author(name="Menace", icon_url="https://cdn.discordapp.com/avatars/1044144223018041344/358cd1a4add10228c4962dd130a7bfd7?size=1024")
        embed.set_footer(text="Patch Date: " + changelog["date"], icon_url="https://cdn.discordapp.com/avatars/1044144223018041344/358cd1a4add10228c4962dd130a7bfd7?size=1024")
                
        for i in range(1, changelog["count"]+1):

            embed.add_field(name="" + changelog["changesTitle"][i-1], value="" + changelog["changesDesc"][i-1], inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command()
    async def purge(self, interaction:discord.Interaction, amount:int):

        if interaction.user.guild_permissions.manage_messages:

            # Delete 'amount' number of messages
            await interaction.channel.purge(limit=amount + 1)
            await interaction.response.send_message(f"{amount} messages deleted.")

        else:

            await interaction.response.send_message("You don't have the necessary permissions to use this command.")


async def setup(bot):
    
    await bot.add_cog(Utility(bot), guilds=[discord.Object(id=675390519714775060)])