import discord, os, typing, aiofiles, json, re, validators
from ast import literal_eval
import datetime as dt
from discord import app_commands
from discord.ext import commands

class Schedule(commands.Cog):

    botIconURL = "https://cdn.discordapp.com/avatars/1044144223018041344/358cd1a4add10228c4962dd130a7bfd7?size=1024"
    dataWasChanged = False
    users = list()

    def __init__(self, bot):

        self.bot = bot

        if "data" not in os.listdir():

            print('"data/users.json" does not exist.\nCreating required dependencies...')
            os.mkdir("data")
            print('"data" created.')
            with open("./data/users.json", "w") as file:

                file.write("[]")
                print('"users.json" created.')
                file.close()

        with open("data/users.json", "r") as file:
                
            Schedule.users = json.loads(file.read())
            file.close()

    @staticmethod
    async def updateUsers():
        
        if Schedule.dataWasChanged:

            text = json.dumps(Schedule.users, indent=4)
            async with aiofiles.open("./data/users.json", "w") as file:
                
                await file.write(text)
                await file.close()

        Schedule.dataWasChanged = False

    # This group is for the "schedule" command series.
    # It's for printing, creating, editing and managing schedules.
    schedule = app_commands.Group(name="schedule", description="A group of commands used to manage schedules.")
    
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

                    for user in Schedule.users:

                        if user["id"] == str(interaction.user.id):

                            user["color"] = value
                            user["updatetime"] = updatedTime

                            Schedule.dataWasChanged = True
                            await Schedule.updateUsers()
                            await interaction.response.send_message("Your **color** was successfully changed on your schedule.\nPlease run **`/schedule view`** to see the changes.")
                            break
                else:

                    await interaction.response.send_message("That was not a valid hex code.")

            case "Icon Image URL":

                if validators.url(value):

                    for user in Schedule.users:

                        if user["id"] == str(interaction.user.id):

                            user["iconURL"] = value
                            user["updatetime"] = updatedTime

                            Schedule.dataWasChanged = True
                            await Schedule.updateUsers()
                            await interaction.response.send_message("Your **icon URL** was successfully changed on your schedule.\nPlease run **`/schedule view`** to see the changes.")
                            break

                else:

                    await interaction.response.send_message("That was not a valid URL.")

            case _:

                if "title" in choice.lower():

                    for user in Schedule.users:

                        if user["id"] == str(interaction.user.id):
                            
                            user["schedule"][choice.lower()] = value
                            user["updatetime"] = updatedTime

                            Schedule.dataWasChanged = True
                            await Schedule.updateUsers()
                            await interaction.response.send_message(f"Your **{choice.lower()}** was successfully changed on your schedule.\nPlease run **`/schedule view`** to see the changes.")
                            break

                else:
    
                    for user in Schedule.users:

                        if user["id"] == str(interaction.user.id):

                            choice = choice.lower().replace(" text", "")
                            user["schedule"][choice] = value
                            user["updatetime"] = updatedTime
    
                            Schedule.dataWasChanged = True
                            await Schedule.updateUsers()
                            await interaction.response.send_message(f"Your **{choice.capitalize()} text** was successfully changed on your schedule.\nPlease run **`/schedule view`** to see the changes.")
                            break

    @schedule.command(description="Ask the bot to start the process to create a new schedule for you.")
    async def create(self, interaction:discord.Interaction, title:str, monday:str, tuesday:str, wednesday:str, thursday:str, friday:str, saturday:str, sunday:str):

        userWasNotFound = True
        for user in Schedule.users:

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
            Schedule.users.append(newSchedule)
            Schedule.dataWasChanged = True
            await Schedule.updateUsers()
            await interaction.response.send_message("### **Your schedule has been successfully created!**\nPlease run **`/schedule view`** and select yourself to see the result!*")

        else:

            await interaction.response.send_message("Sorry, it seems that you already have a schedule created for you.\nIf you want to change that schedule, please run **`/schedule edit`**.")

    @schedule.command(description="Ask the bot to print out a schedule.")
    async def view(self, interaction:discord.Interaction, member:discord.Member):

        await Schedule.updateUsers()

        message = "There seems to be nothing in the database at the moment. Please create a schedule."

        for user in Schedule.users:

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
                
                Schedule.dataWasChanged = True
                message = "A matching user was not found. Please make sure you chose the right member.\nIf you are that member, try creating a schedule with the **`/schedule create`** command."

        try:

            await interaction.response.send_message(embed=message)

        except Exception as e:

            await interaction.response.send_message(message)

    
        
async def setup(bot):
    
    await bot.add_cog(Schedule(bot), guilds=[discord.Object(id=675390519714775060)])