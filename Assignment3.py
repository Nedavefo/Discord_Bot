import os
import csv
import discord
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('token.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
fname = "memberLogon.csv"

intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)

# Asynchronous function to write data to a CSV file
async def write_to_csv(filename, data):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Event triggered when the bot has successfully connected to Discord
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)  # Get the server object
    print(f"{client.user} is online on {guild.name}!")  # Print connection message

    await write_to_csv(fname, ['Member Names: '])  # Write header to CSV file
    for member in guild.members:  # Iterate over members in the server
        await write_to_csv(fname, [member.name])  # Write member names to CSV
        print(f"- {member.name}")  # Print member names

# Event triggered when a new member joins the server
@client.event
async def on_member_join(member):
    join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
    await write_to_csv(fname, [member.name, join_date])  # Write member join event to CSV
    print(f"Join date of {member.name} has been saved to {fname}")

# Event triggered when a member leaves the server
@client.event
async def on_member_remove(member):
    guild = discord.utils.get(client.guilds, name=GUILD)  # Get the server object
    print(f"{member} have left the server.")  # Print departure message
    left_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
    
    await write_to_csv(fname, [member.name, "Left ", left_date])  # Write member leave event to CSV
    canal_general = client.get_channel(808371005751033909)  # Get the general channel
    await canal_general.send(f"Goodbye, {member}! We will miss you :(")  # Send goodbye message to general channel
    for member in guild.members:  # Iterate over members in the server
        await write_to_csv(fname, [member.name])  # Write member names to CSV
        print(f"- {member.name}")

client.run(TOKEN)