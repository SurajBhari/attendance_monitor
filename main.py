from json import load
from datetime import date, datetime, timedelta
from discord import Webhook, RequestsWebhookAdapter, Embed

schedule = load(open('schedule.json'))

"""
# For testing purposes
"""
curr_time = datetime(2022, 4, 28, 9, 0 , 0)


difference = timedelta(hours=5, minutes=30)
curr_time = datetime.utcnow() + difference
curr_date = curr_time.date()
time_str = curr_time.strftime("%H:%M")
day = curr_time.strftime("%A").lower()
print(time_str)

try:
    todays_schedule = schedule["actual_schedule"][day]
except KeyError:
    print("No schedule for today")
    exit()

try:
    current_class = todays_schedule[time_str]
except KeyError:
    print("No class at this time")
    exit()

webhook = Webhook.from_url(schedule["config"]["webhook_url"], adapter=RequestsWebhookAdapter())

embed = Embed(title=f"{current_class}", color=0x00ff00)
embed.add_field(name=f"At {time_str}", value="?",inline=False)
embed.add_field(name=f"On {curr_date.strftime('%A, %d/%m/%Y')}", value="?", inline=False)

webhook.send(embed=embed)