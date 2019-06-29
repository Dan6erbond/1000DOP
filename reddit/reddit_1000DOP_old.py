import praw
import datetime
import sys
from requests.exceptions import ConnectionError, HTTPError
from time import sleep

reddit = praw.Reddit("1000DOP")
subreddit = reddit.subreddit("1000DaysOfPractice")

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def update_flairs():
    while True:
        date_started = datetime.datetime.utcnow()
        try:
            for comment in subreddit.stream.comments():
                if comment is None:
                    continue
                
                in_right_thread = "Daily" in comment.submission.link_flair_text
                parent_comment = "t3" in comment.parent_id
                new = datetime.datetime.utcfromtimestamp(comment.created_utc) > date_started
        
                if in_right_thread and parent_comment and new:
                    flair = next(subreddit.flair(comment.author.name))["flair_text"]
                
                    if flair is not None:
                        old_flair = flair
                    else:
                        old_flair = ""
                    old_flair = old_flair
                        
                    days = 0
                    
                    if flair is not None and flair.endswith("Day(s)"):
                        days_string = ""
                        end = flair.split(" | ")[len(flair.split(" | "))-1]
                        
                        for char in end:
                            if char in "0123456789":
                                days_string += char
                                
                        days = int(days_string)
                        flair = flair.replace(" | {}".format(end), "")
                    elif flair is None:
                        flair = ""
                        
                    days += 1
                    flair = "{} | {} Day(s)".format(flair, days)
        
                    author = comment.author.name
                    
                    print("{}: {} -> {}".format(author.translate(non_bmp_map), old_flair.translate(non_bmp_map), flair).translate(non_bmp_map))
                    subreddit.flair.set(author, flair)
        except ConnectionError:
            date_started = datetime.datetime.utcnow()
            sleep(30)
            full = traceback.format_exc()
            logging.warning("Connection error: %s", full)
        except HTTPError:
            date_started = datetime.datetime.utcnow()
            sleep(30)
            full = traceback.format_exc()
            logging.warning("HTTP error %s" % full)

def set_flairs_first_time():
    users = []

    for submission in subreddit.search('flair_name:"Daily"'): # iterate through all daily submissions
        if submission.comments is not None: # check if the submission has any comments
            for comment in submission.comments: # iterate through all top-level comments
                if comment.author is not None: # make sure the author still exists
                    users.append(comment.author.name)

    userSet = set(users)

    for user in userSet:
        counter = 0
        for user1 in users:
            if user1 == user:
                counter += 1
        flair = next(subreddit.flair(user))["flair_text"]
        old_flair = flair
        if flair is not None and "Day(s)" in flair:
            end = flair.split(" | ")[len(flair.split(" | "))-1]
            flair = flair.replace(end,"")
        elif flair is None:
            flair = ""
        flair += " | " + str(counter) + " Day(s)"
        print(user.translate(non_bmp_map) + ": " + old_flair.translate(non_bmp_map) + " -> " + flair.translate(non_bmp_map))
        subreddit.flair.set(user, flair)

# set_flairs_first_time()
update_flairs()
