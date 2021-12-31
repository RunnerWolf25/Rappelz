
import os
import discord
import pyodbc
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
DISCORD_TOKEN = ""



client = discord.Client()

@client.event 
async def on_ready():
    print("Connecting to SQL server.")
    try:
        global conn
        conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=localhost;'
                        'Database=Telecaster;'
                        'Trusted_Connection=yes;')
    except:
        print('Couldn\'t connect to the SQL server.')
        quit()

    print(f'Loaded successfully as {client.user}')



@client.event   
async def on_message(msg):


    if msg.content == "!help":
        await msg.channel.send(f"The current commands are:\n!gold\n!lvl")
#lvl------------------------------------------------------------------------------
    if msg.content == "!lvl":
        cursor = conn.cursor()
        cursor.execute("SELECT name , lv from dbo.Character order by lv DESC")
        data = cursor.fetchall()
        name = []
        level = []
        message = str()

        for row in data:
            name.append(row.name)
            level.append(row.lv)


        for i, (x,y) in enumerate(zip(name,level)):
            if i ==3:
                break
            message = (f"{message}\nRank{i+1}\nname : {x:10} level: {y}")
        message = (f"```{message}```")
        await msg.channel.send(message)
#lvl------------------------------------------------------------------------------


#Gold -----------------------------------------------------------------------------
    if msg.content == "!gold":
        cursor = conn.cursor()
        cursor.execute("SELECT name , gold from dbo.Character order by gold DESC")
        data = cursor.fetchall()
        name = []
        gold = []
        message = str()

        for row in data:
            name.append(row.name)
            gold.append(row.gold)
        
        for i, (x,y) in enumerate(zip(name,gold)):
            if i == 3:
                break
            message = (f"{message}\nRank{i+1:3}\n name: {x:10} ruppee: {y:3}")

        message = f"```{message}```"
        await msg.channel.send(message)
#Gold -----------------------------------------------------------------------------
client.run(DISCORD_TOKEN) 
