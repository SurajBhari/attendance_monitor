from discord.ext import commands
from discord import Intents, File
from json import load, dump
from datetime import date, datetime, timedelta
from show_data import get_data


config = load(open('schedule.json'))["config"]
token = config["token"]

intents = Intents.default()
intents.members = True


bot = commands.Bot(command_prefix = "asdasdaasdsa", intents=intents)
reactions = ["👍", "👎", "❌"]

@bot.event
async def on_ready():
    print("Am ready to gooooo")
    bot.self_info = await bot.application_info()
    bot.owner = bot.self_info.owner

@bot.event
async def on_message(message):
    if message.author == bot.owner:
        if message.content == "show data":
            string, files_list = get_data()
            await message.channel.send(string)
            for file in files_list:
                await message.channel.send(file=File(file))

    if message.author.id == config["webhook_id"]:
        print("Got a message from the webhook")
        message = await bot.owner.send(content = message.content, embed= message.embeds[0])
        for reaction in reactions:
            await message.add_reaction(reaction)
        
        def check(reaction, user):
            return str(reaction.emoji) in reactions and reaction.message.id== message.id and user.id == bot.owner.id
                
        reaction, user = await bot.wait_for("reaction_add", check=check)
        print("Got a response")
        state = ""
        if str(reaction.emoji) == reactions[0]:
            print("Accepted")
            state = "Taken"
        elif str(reaction.emoji) == reactions[1]:
            print("Rejected")
            state = "Not Taken"
        else:
            print("Class Cancelled")
            state = "Cancelled/Teacher Absent"
        
        # extract webook info
        embed = message.embeds[0]
        class_name = embed.title
        class_time = embed.description
        await message.delete()
        # process the response
        responses = load(open("responses.json"))
        difference = timedelta(hours=5, minutes=30)
        curr_time = datetime.utcnow() + difference
        curr_date = curr_time.date()
        dic = { 
            "class_name": class_name,
            "class_time": embed.fields[0].name,
            "class_date": curr_date.strftime("%d/%m/%Y"),
        }
        if state == "Taken":
            responses["taken"].append(dic)
        elif state == "Not Taken":
            responses["not_taken"].append(dic)
        elif state == "Cancelled/Teacher Absent":
            responses["cancelled"].append(dic)
        dump(responses, open("responses.json", "w"), indent=4) 

bot.run(token)