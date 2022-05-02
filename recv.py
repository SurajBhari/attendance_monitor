from discord.ext import commands
from discord import Intents, File
from json import load, dump
from datetime import date, datetime, timedelta
from show_data import get_data


config = load(open('schedule.json'))["config"]
token = config["token"]

intents = Intents.default()
intents.members = True


bot = commands.Bot(command_prefix = ">", intents=intents)
reactions = ["👍", "👎", "❌"]

@bot.event
async def on_ready():
    print("Am ready to gooooo")
    bot.self_info = await bot.application_info()
    bot.owner = bot.self_info.owner

@bot.command(name="show")
async def show(ctx):
    if ctx.author != bot.owner:
        return
    string, files_list = get_data()
    await ctx.send(string)
    for file in files_list:
        await ctx.send(file=File(file))

@bot.command(name="end")
async def end(ctx):
    if ctx.author != bot.owner:
        return
    await ctx.send("Are you sure you want to end the current semester right here and delete all the previous records ?")
    message = await bot.wait_for("message", check=lambda message: message.author == ctx.author)
    if message.content == "yes":
        with open("responses.json", "r") as f:
            data = load(f)
        with open('responses.bak.json', 'w') as f:
            dump(data, f)
        with open('responses.json', 'w') as f:
            dump({}, f)
        await ctx.send("Done")

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
        embed = message.embeds[0]
        def check(reaction, user):
            return str(reaction.emoji) in reactions and reaction.message.id== message.id and user.id == bot.owner.id
                
        reaction, user = await bot.wait_for("reaction_add", check=check)
        print("Got a response")
        state = ""
        if str(reaction.emoji) == reactions[0]:
            print("Accepted")
            state = "Taken"
            embed.color = 0x00ff00
        elif str(reaction.emoji) == reactions[1]:
            print("Rejected")
            state = "Not Taken"
            embed.color = 0xff0000
        else:
            print("Class Cancelled")
            state = "Cancelled/Teacher Absent"
            embed.color = 0xffff00
        
        # extract webook info
        class_name = embed.title
        class_time = embed.fields[0].name
        await message.delete()
        embed.title = f"{class_name} - {state}"
        embed.description = f"{class_time}"
        # process the response
        responses = load(open("responses.json"))
        difference = timedelta(hours=5, minutes=30)
        curr_time = datetime.utcnow() + difference
        curr_date = curr_time.date()
        dic = { 
            "class_name": class_name,
            "class_time": class_time,
            "class_date": curr_date.strftime("%d/%m/%Y"),
        }
        if state == "Taken":
            responses["taken"].append(dic)
        elif state == "Not Taken":
            responses["not_taken"].append(dic)
        elif state == "Cancelled/Teacher Absent":
            responses["cancelled"].append(dic)
        dump(responses, open("responses.json", "w"), indent=4) 
        await message.channel.send(content="Successfully logged your input", embed=embed)
    await bot.process_commands(message)

bot.run(token)