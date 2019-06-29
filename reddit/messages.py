import praw
import datetime
import sys
# from requests.exceptions import ConnectionError, HTTPError
from time import sleep

reddit = praw.Reddit("1000DOP")
subreddit = reddit.subreddit("1000DaysOfPractice")

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def read_pms():
    date_started = datetime.datetime.utcnow()
    while True:
        try:
            for item in reddit.inbox.stream():
                message = None
                if isinstance(item, praw.models.Message):
                    message = item
                if message is None:
                    continue

                new = datetime.datetime.utcfromtimestamp(message.created_utc) > date_started

                '''if "update" in message.subject.lower() and new:
                    limit = 0
                    for submission in subreddit.search('flair_name:"Daily"'): # iterate through all daily submissions
                        limit += 1
                        if submission.comments is not None: # check if the submission has any comments
                            for comment in submission.comments: # iterate through all top-level comments
                                if comment.author is not None and comment.author == message.author: # make sure the author still exists
                                    limit -= 1
                                
                    flair = next(subreddit.flair(comment.author.name))["flair_text"]'''
                if "flair" in message.subject.lower() and new:
                    partitions = []
                    assign_flair = True
                    
                    limit = 0
                    for submission in subreddit.search('flair_name:"Daily"'): # iterate through all daily submissions
                        if submission.comments is not None: # check if the submission has any comments
                            for comment in submission.comments: # iterate through all top-level comments
                                if comment.author is not None and comment.author == message.author: # make sure the author still exists
                                    limit += 1
                    
                    message_content = message.body.replace(" ", "") + " " # removes spaces and adds one to the end
                    emoji = ""
                    days = "0"
                    
                    for y in range(0,len(message_content)): # scan through the message's characters
                        character = message_content[y]
                        if character in "-0123456789":
                            days += character
                        if character.encode('unicode-escape').decode('utf-8').startswith("\\U") or y == len(message_content)-1: # if we hit an emoji or the end
                            if emoji != "": # if we have an emoji to work with
                                try:
                                    days = int(days)
                                    if days > limit:
                                        assign_flair = False
                                except ValueError:
                                    days = 0
                                partitions.append("{} {} Day(s)".format(emoji, days))
                                emoji = ""
                                days = "0"
                            if character.encode('unicode-escape').decode('utf-8').startswith("\\U"): # if we hit an emoji
                                emoji = character
                            
                    flair = ""
                    for partition in partitions:
                        flair += " | " + partition
                    flair = flair[3:len(flair)]

                    if assign_flair:
                        print('Assigned "{}" to {}.'.format(flair.translate(non_bmp_map), message.author.name))
                        message.author.message('Flair assigned!', 'Thanks for messaging. Your new flair is "{}".'.format(flair))
                        subreddit.flair.set(message.author, flair)
                    else:
                        print('Didn\'t assign "{}" to {}.'.format(flair.translate(non_bmp_map), message.author.name))
                        message.author.message('Flair not assigned!', 'Thanks for messaging. Unfortunately, your new flair ({}) wasn\'t assigned becauseeither the requested number(s) exceeded limits implemented by my developer, or you have not logged the requested number of days in the Daily Practice Log threads.\nPlease contact the moderators of this subreddit if you feel this was an error.".'.format(flair))
        except Exception as e:
            date_started = datetime.datetime.utcnow()
            print("{}: {}".format(type(e), e))
            sleep(30)
        '''                                    
        except ConnectionError as e:
            date_started = datetime.datetime.utcnow()
            print("{}: {}".format(type(e), e)
            sleep(30)
        except HTTPError as e:
            date_started = datetime.datetime.utcnow()
            print("{}: {}".format(type(e), e)
            sleep(30)
        except praw.exceptions.PRAWException:
            date_started = datetime.datetime.utcnow()
            sleep(30)
            full = traceback.format_exc()
            logging.warning("PRAW Exception: %s" % full)
        except prawcore.exceptions.PrawcoreException:
            date_started = datetime.datetime.utcnow()
            sleep(30)
            full = traceback.format_exc()
            logging.warning("PRAW Core Exception: %s" % full)
        '''

read_pms()
