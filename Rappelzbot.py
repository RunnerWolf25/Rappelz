from logging import currentframe # Likely not needed.
import os                        # likely not needed
import discord
import time
import pyodbc

# try to get token from file stored in the base directory.
# fail gracefully if file not found
token_file = 'Token.txt'
try:
    # Reads the file that's defined below here, If it's in the same folder only add the name + extension)
    with open(token_file) as r:
        DISCORD_TOKEN = (r.readline())
except OSError as err:
    print(f'[ERROR]: {token_file} not found')
    quit()



lasttime = 0 # stores the last unix timestamp when the bot accessed the database to prevent spam
conn = None  # will later represent the connection to the database


# define discord bot
client = discord.Client()

@client.event
async def on_ready():
    '''
    this method is called when the bot is ready to do bot stuff
    sets up a connection to the player database and logs status to console
    '''
    print('Connecting to SQL server.')
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
    '''
    on message recieve, process message.
    this is the bulk of the bot's functionality
    '''
# Help command -------------------------------------------------------------
    if msg.content == '!help':
        await msg.channel.send('The current commands are:\n!gold\n!lvl')
        return
# Help command -------------------------------------------------------------

# Time block ( Anything past here has a time block of 10 seconds if it has time.time() on the lasttime 
# defined )
# Time block------------------------------------
    curenttime = time.time()
    global lasttime
    if (lasttime + 10) >= (curenttime):
        return

    match msg.content:
#------------------------------------------<lvl>----------------------------------
        case `!lvl`:
            cursor = conn.cursor()
            cursor.execute('SELECT TOP(3) name , lv from dbo.Character order by lv DESC')
            data    = cursor.fetchall()
            name    = []
            level   = []
            message = str()

            for row in data:
                name.append(row.name)
                level.append(row.lv)


            for rank, (x, y) in enumerate(zip(name,level)):

                message = (f'{message}\nRank {rank+1}\nname : {x:10} level: {y}')
            message = (f'```{message}```')
            await msg.channel.send(message)
#------------------------------------------</lvl>---------------------------------

#------------------------------------------<Gold>---------------------------------
        case `!gold`:
            cursor = conn.cursor()
            cursor.execute('SELECT TOP(3) name , gold from dbo.Character order by gold DESC')
            data = cursor.fetchall()
            name = []
            gold = []
            message = str()

            for row in data:
                name.append(row.name)
                gold.append(row.gold)

            for rank, (x, y) in enumerate(zip(name, gold)):

                message = (f'{message}\nRank{rank+1:3}\n name: {x:10} ruppee: {y:3}')

            message = f'```{message}```'
            await msg.channel.send(message)
#------------------------------------------</Gold>---------------------------------

    lasttime = time.time()



# run discord bot
client.run(DISCORD_TOKEN)
