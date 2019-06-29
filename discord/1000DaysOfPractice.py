import discord
import praw
import asyncio
import time
import configparser
from datetime import datetime
from discord.ext.commands import Bot

reddit = praw.Reddit("1000DOP")
subreddit = reddit.subreddit("1000DaysOfPractice")

client = Bot("!")
flair = ""

@client.event
async def on_message(message):
    global flair
    
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith("!channels"):
        new_message = ""
        for channel in message.server.channels:
            async for msg in client.logs_from(channel, limit = 1):
                diff = datetime.utcnow() - msg.timestamp
                diff = int(diff.days * 24 + diff.seconds / 60 / 60)
                new_message += "\n\nLast message in {0.mention} {1} hour(s) ago by {2.author.mention}".format(channel,diff,msg)
        await client.send_message(message.channel, new_message)
        # await client.delete_channel(client.get_channel("539348903544487958"))
                
    if message.content.startswith("!report"):
        async for msg in client.logs_from(client.get_channel("538604760471699460"), limit = 100):
            await client.delete_message(msg)
        users = []

        hours = "0"
        for character in message.content:
            if character in "01233456789":
                hours += character
        hours = max(24.0, float(hours)) # at least the past 24 hours
        
        for comment in subreddit.comments():
            comment_date = datetime.utcfromtimestamp(comment.created_utc)
            current_date = datetime.utcnow()
            diff = current_date - comment_date
            diff = diff.days * 24 + diff.seconds / 60 / 60
            if "t3" in comment.parent_id and "Daily" in comment.submission.link_flair_text and diff < hours:
                users.append(comment.author.name)
                if "statistics" not in message.content and "stats" not in message.content:
                    await client.send_message(client.get_channel("538604760471699460"),"{} - {}: {}{}".format(comment_date, comment.author.name, comment.submission.url, comment.id))
                
        usersDistinguished = set(users)
        stats=""
        for user in usersDistinguished:
            count = 0
            for user1 in users:
                if user == user1:
                    count+=1
            stats+="\n\n{} {} parent-comment(s) in daily thread(s) within the past {} hours.".format(user, count, hours)
        await client.send_message(client.get_channel("538604760471699460"), stats)

    if message.content.startswith("!clear") and "mod" in [y.name.lower() for y in message.author.roles]:
        amt = "0"
        for x in message.content:            
            if x in "0123456789":
                amt += x
        if "all" in message.content:
            amt = 100
        else:
            amt = min(100,int(amt)+1)
        async for msg in client.logs_from(message.channel, limit = amt):
            await client.delete_message(msg)
        await client.send_message(message.channel, "{0.author.mention} deleted {1} messages!".format(message, amt))

    if message.content.startswith("!create_flair"):
        partitions = []
        
        message_content = message.content.replace(" ", "") + " " # removes spaces and adds one to the end
        emoji = ""
        days = "0"
        limit = 100
        for y in range(0,len(message_content)): # scan through the message's characters
            character = message_content[y]
            if character in "0123456789":
                days += character
            if character.encode('unicode-escape').decode('utf-8').startswith("\\U") or y == len(message_content)-1: # if we hit an emoji or the end
                if emoji != "": # if we have an emoji to work with
                    days = min(limit,int(days))
                    partitions.append("{} {} Day(s)".format(emoji, days))
                    emoji = ""
                    days = "0"
                if character.encode('unicode-escape').decode('utf-8').startswith("\\U"): # if we hit an emoji
                    emoji = character
                
        flair = ""
        for partition in partitions:
            flair += " | " + partition
        flair = flair[3:len(flair)]
        await client.send_message(message.channel, flair)

    if message.content.startswith("!update_flair"):
        message_content = message.content.replace(" ", "") + " " # removes spaces and adds one to the end
        partitions = flair.split("|") # split the flair we have into the bits ("|" is a separator)
        emoji = ""
        increase_days = "0"
        limit = 100
        for y in range(0,len(message_content)): # scan through the message's characters
            character = message_content[y]
            if character in "0123456789":
                increase_days += character
            if character.encode('unicode-escape').decode('utf-8').startswith("\\U") or y == len(message_content)-1: # if we hit an emoji or the end
                if emoji != "": # if we have an emoji to work with
                    increase_days = min(limit,max(1,int(increase_days)))
                    for x in range(0,len(partitions)): # scan through the flair's partitions
                        if emoji in partitions[x]:
                            days = "0"
                            for partition_character in partitions[x]:
                                if partition_character in "0123456789":
                                    days += partition_character
                            days = int(days) + increase_days
                            partitions[x] = "{} {} Day(s)".format(emoji, days)
                    emoji = ""
                    increase_days = "0"
            if character.encode('unicode-escape').decode('utf-8').startswith("\\U"): # if we hit an emoji
                emoji = character
                    
        flair = ""
        for partition in partitions:
            partition = partition.strip()
            flair += " | " + partition
        flair = flair[3:len(flair)] # Removes the first " | "
        await client.send_message(message.channel, flair) # sends the flair to the channel

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

config = configparser.ConfigParser()
config.read("discord.ini")
client.run(config["1000DOP"]["Token"])
