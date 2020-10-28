# bot.py
import os
import itertools
import csv
import discord
import datetime
from dotenv import load_dotenv
from collections import Counter #This is needed to use the Counter method later on

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')   #These two are our secret tokens to connect our bot to discord using the keys in .env
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD) #Not sure what "name=GUILD" is for but this gets our server basically and assigns it
    channel = client.get_channel(164580034269413376)     #Same thing as above but for channel

    msg_user = []       #Setting our variable to a blank list
    msg_content = []
    msg_time = []
    msg_info = []


    counter = 0         #Setting our counter to 0
    async for message in channel.history(limit=200):  #This async command gets the messages in a given channel
            msg_time.append(message.created_at)
            msg_user.append(message.author.name)    #Appends message author names to 'msg_user'
            msg_content.append(message.content)
            counter += 1

#     for item in itertools.chain(msg_user, msg_content):
#             msg_info.append(item)

    msg_info = list(zip(msg_user, msg_content, msg_time))    
    messages = await channel.history(limit=1).flatten() #This is kinda useless rn, but it gets all the messages and puts them into list form (including all msg info)
    user_msg_count = Counter(msg_user)  #Use Counter to get a count of unique authors from our msg_user list -- Not neccessary since jupyter can do this

    
    with open('user_msg_count.csv', 'w', encoding='utf-8') as f:           #Code that uses csv import above, takes variable w/ what we want csv. The w is the 'dialect'? fkn encoding for that one guy
            writer = csv.writer(f)                       #setting up the writer
            writer.writerow(['user_name', 'msg_content', 'msg_time' ])
            writer.writerows(msg_info)     #We use writerows witch could be DictWriter but w/ writerow instead?
            
        

    print(
        f'{client.user} has connected to Discord!\n'
        f'Connected to {guild.name}(id: {guild.id})\n'
        f'Channel list: {channel.name}\n'
        f'Amount of messages indexed: {(len(msg_user))}\n'  
        f'number msgs sent by each user: {user_msg_count}\n'
        f'content of messages: *OFF* \n'
        f'user and content and time: *OFF* \n'
        )

client.run(TOKEN)