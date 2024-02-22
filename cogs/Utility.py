import discord, os, typing, aiofiles, json, re, validators
from ast import literal_eval
import datetime as dt
from discord import app_commands
from discord.ext import commands

# These commands are used for various functions that are menat to be more like tools or stations.
class Utility(commands.Cog):

    botIconURL = "https://cdn.discordapp.com/avatars/1044144223018041344/358cd1a4add10228c4962dd130a7bfd7?size=1024"
    dataWasChanged = False
    users = list()

    def __init__(self, bot):

        self.bot = bot
        with open("./data/users.json", "r") as file:
                
            Utility.users = json.loads(file.read())
            file.close()

    @staticmethod
    async def updateUsers():
        
        if Utility.dataWasChanged:

            test = json.dumps(Utility.users, indent=4)
            async with aiofiles.open("./data/users.json", "w") as file:
                
                await file.write(test)
                await file.close()

        Utility.dataWasChanged = False

    # This group is for the "schedule" command series.
    # It's for printing, creating, editing and managing schedules.
    schedule = app_commands.Group(name="schedule", description="A group of commands used to manage schedules.")

    @app_commands.command()
    async def help(self, interaction:discord.Interaction, command:typing.Literal["schedule"]):

        match command:

            case "schedule":

                embed = discord.Embed(title="Schedule", description="A group of commands used to manage schedules.", timestamp=dt.datetime.now(), color=0x2a783f)
                embed.set_author(name="Menace", icon_url="https://cdn.discordapp.com/avatars/1044144223018041344/358cd1a4add10228c4962dd130a7bfd7?size=1024")
                embed.add_field(name="\"view\"", value="`member`: the user who's schedule you want to view.")
                embed.add_field(name="\"create\"", value="This has a number of fields but each field is self explanitory.")
                embed.add_field(name="\"edit\"", value="`choice`: \nFor \"Hex Code Color\", make sure to use something like [Google's color picker](https://g.co/kgs/a5zGFqo).\nIf you want to get your profile picture URL, use something like [Toolscord](https://toolscord.com) to grab your discord URL. Only image URLs will work for your icon.")

                await interaction.response.send_message(embed=embed)

    @schedule.command(description="Change different parts of your schedule.")
    async def edit(self, interaction:discord.Interaction, choice:typing.Literal["Title", "Subtitle", "Hex Code Color", "Icon Image URL", "Monday Text", "Tuesday Text", "Wednesday Text", "Thursday Text", "Friday Text", "Saturday Text", "Sunday Text"], value:str):

        currentDay = str(dt.datetime.now().day)
        currentMonth = dt.datetime.strptime(str(dt.datetime.now().month), "%m").strftime("%b")
        currentYear = str(dt.datetime.now().year)
        updatedTime = currentMonth + ". " + currentDay + ", " + currentYear
        match choice:

            case "Hex Code Color":

                hexCode = re.compile(r"#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$")

                if bool(re.match(hexCode, value)):

                    value = value.replace("#", "0x")

                    for user in Utility.users:

                        if user["id"] == str(interaction.user.id):

                            user["color"] = value
                            user["updatetime"] = updatedTime

                            Utility.dataWasChanged = True
                            await Utility.updateUsers()
                            await interaction.response.send_message("Your **color** was successfully changed on your schedule.\nPlease run **`/schedule view`** to see the changes.")
                            break
                else:

                    await interaction.response.send_message("That was not a valid hex code.")

            case "Icon Image URL":

                if validators.url(value):

                    for user in Utility.users:

                        if user["id"] == str(interaction.user.id):

                            user["iconURL"] = value
                            user["updatetime"] = updatedTime

                            Utility.dataWasChanged = True
                            await Utility.updateUsers()
                            await interaction.response.send_message("Your **icon URL** was successfully changed on your schedule.\nPlease run **`/schedule view`** to see the changes.")
                            break

                else:

                    await interaction.response.send_message("That was not a valid URL.")

            case _:

                if "title" in choice.lower():

                    for user in Utility.users:

                        if user["id"] == str(interaction.user.id):
                            
                            user["schedule"][choice.lower()] = value
                            user["updatetime"] = updatedTime

                            Utility.dataWasChanged = True
                            await Utility.updateUsers()
                            await interaction.response.send_message(f"Your **{choice.lower()}** was successfully changed on your schedule.\nPlease run **`/schedule view`** to see the changes.")
                            break

                else:
    
                    for user in Utility.users:

                        if user["id"] == str(interaction.user.id):

                            choice = choice.lower().replace(" text", "")
                            user["schedule"][choice] = value
                            user["updatetime"] = updatedTime
    
                            Utility.dataWasChanged = True
                            await Utility.updateUsers()
                            await interaction.response.send_message(f"Your **{choice.capitalize()} text** was successfully changed on your schedule.\nPlease run **`/schedule view`** to see the changes.")
                            break

    @schedule.command(description="Ask the bot to start the process to create a new schedule for you.")
    async def create(self, interaction:discord.Interaction, title:str, monday:str, tuesday:str, wednesday:str, thursday:str, friday:str, saturday:str, sunday:str):

        userWasNotFound = True
        for user in Utility.users:

            if user["id"] == str(interaction.user.id):

                userWasNotFound = False
                break

        if userWasNotFound:

            currentDay = str(dt.datetime.now().day)
            currentMonth = dt.datetime.strptime(str(dt.datetime.now().month), "%m").strftime("%b")
            currentYear = str(dt.datetime.now().year)
            newSchedule = {
                "id": str(interaction.user.id),
                "name": interaction.user.name,
                "schedule": {
                    "title": title,
                    "subtitle": "",
                    "monday": monday,
                    "tuesday": tuesday,
                    "wednesday": wednesday,
                    "thursday": thursday,
                    "friday": friday,
                    "saturday": saturday,
                    "sunday": sunday,
                },
                "updatetime": currentMonth + ". " + currentDay + ", " + currentYear,
                "color": "0xFFFFFF",
                "iconURL": ""
            }
            Utility.users.append(newSchedule)
            Utility.dataWasChanged = True
            await Utility.updateUsers()
            await interaction.response.send_message("### **Your schedule has been successfully created!**\nPlease run **`/schedule view`** and select yourself to see the result!*")

        else:

            await interaction.response.send_message("Sorry, it seems that you already have a schedule created for you.\nIf you want to change that schedule, please run **`/schedule edit`**.")

    @schedule.command(description="Ask the bot to print out a schedule.")
    async def view(self, interaction:discord.Interaction, member:discord.Member):

        await Utility.updateUsers()

        message = "There seems to be nothing in the database at the moment. Please create a schedule."

        for user in Utility.users:

            if user["id"] == str(member.id):

                message = discord.Embed(title=f"**{user['schedule']['title']}**", 
                                        description=f"*{user['schedule']['subtitle']}*",
                                        color=literal_eval(user['color']),
                                        )
                message.set_author(name=member.name, icon_url=member.avatar.url)
                message.set_thumbnail(url=user['iconURL'])
                message.add_field(name="Monday:", value=user['schedule']['monday'], inline=False)
                message.add_field(name="Tuesday:", value=user['schedule']['tuesday'], inline=False)
                message.add_field(name="Wednesday:", value=user['schedule']['wednesday'], inline=False)
                message.add_field(name="Thursday:", value=user['schedule']['thursday'], inline=False)
                message.add_field(name="Friday:", value=user['schedule']['friday'], inline=False)
                message.add_field(name="Saturday:", value=user['schedule']['saturday'], inline=False)
                message.add_field(name="Sunday:", value=user['schedule']['sunday'], inline=False)
                message.set_footer(text=f"Last updated: {user['updatetime']}", icon_url=self.botIconURL)
                break
            
            else:
                
                Utility.dataWasChanged = True
                message = "A matching user was not found. Please make sure you chose the right member.\nIf you are that member, try creating a schedule with the **`/schedule create`** command."

        try:

            await interaction.response.send_message(embed=message)

        except Exception as e:

            await interaction.response.send_message(message)

    
        
async def setup(bot):
    
    await bot.add_cog(Utility(bot), guilds=[discord.Object(id=1165738081945653369), discord.Object(id=675390519714775060)])