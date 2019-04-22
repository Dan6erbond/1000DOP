import praw
import datetime
import sys
# from requests.exceptions import ConnectionError, HTTPError
from time import sleep

reddit = praw.Reddit("1000DOP")
subreddit = reddit.subreddit("1000DaysOfPractice")

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

motivational_messages = ["We may encounter many defeats but we must not be defeated.",
                         "Our greatest glory is not in never falling, but in rising every time we fall.",
                         "All our dreams can come true, if we have the courage to pursue them.",
                         "It does not matter how slowly you go as long as you do not stop.",
                         "Believe in yourself. You are braver than you think, more talented than you know, and capable of more than you imagine.",
                         "Your true success in life begins only when you make the commitment to become excellent at what you do.",
                         "Definiteness of purpose is the starting point of all achievement.",
                         "Success means doing the best we can with what we have. Success is the doing, not the getting; in the trying, not the triumph. Success is a personal standard, reaching for the highest that is in us, becoming all that we can be.",
                         "I attribute my success to this: I never gave or took any excuse.",
                         "I am not a product of my circumstances. I am a product of my decisions.",
                         "It’s not about perfect. It’s about effort. And when you bring that effort every single day, that’s where transformation happens. That’s how change occurs.",
                         "Success is no accident. It is hard work, perseverance, learning, studying, sacrifice and most of all, love of what you are doing or learning to do.",
                         "Strength doesn’t come from what you can do. It comes from overcoming the things you once thought you couldn’t.",
                         "Go confidently in the direction of your dreams. Live the life you have imagined.",
                         "Setting goals is the first step into turning the invisible into the visible.",
                         "Remember that not getting what you want is sometimes a wonderful stroke of luck.",
                         "Twenty years from now you will be more disappointed by the things you didn’t do than by the things you did.",
                         "Your time is limited, so don’t waste it living someone else’s life.",
                         "Challenges are what make life interesting and overcoming them is what makes life meaningful.",
                         "You will never find time for anything. If you want time you must make it.",
                         "The greatest danger for most of us is not that our aim is too high and we miss it, but that it is too low and we reach it."]
motivational_messages_keywords = ["give up"]

def read_comments():
    date_started = datetime.datetime.utcnow()
    while True:
        try:
            file = open("comments.txt")
            content = file.read()
            file.close()
            for comment in subreddit.stream.comments():
                in_daily_thread = "Daily" in comment.submission.link_flair_text
                parent_comment = "t3" in comment.parent_id
                # new = datetime.datetime.utcfromtimestamp(comment.created_utc) > date_started

                if comment is not None and comment.author is not None and comment.id not in content and in_daily_thread and parent_comment: # and new:
                    file = open("comments.txt", "a")
                    print(comment.id)
                    file.write(comment.id + "\n")
                    file.close()

                    flair = next(subreddit.flair(comment.author.name))["flair_text"]

                    if flair is None:
                        flair = ""

                    old_flair = flair

                    emojis = set()
                    for character in comment.body:
                        if character.encode('unicode-escape').decode('utf-8').startswith("\\U"):
                            emojis.add(character)

                    highest_day = 0
                    partitions = flair.split("|")
                    for emoji in emojis:
                        for x in range(0,len(partitions)): # scan through the flair's partitions
                            if emoji in partitions[x]:
                                days = "0"
                                for partition_character in partitions[x]:
                                    if partition_character in "0123456789":
                                        days += partition_character
                                days = int(days)+1
                                if days > highest_day:
                                    highest_day = days
                                partitions[x] = "{} {} Day(s)".format(emoji, days)

                    flair = ""
                    for partition in partitions:
                        partition = partition.strip()
                        flair += " | " + partition
                    flair = flair[3:len(flair)] # Removes the first " | "
                    if old_flair != flair:
                        template_id = get_template_id(highest_day)
                        subreddit.flair.set(comment.author, flair, flair_template_id=template_id)
                        print("Replaced {} with {} for {}.".format(old_flair, flair, comment.author.name).translate(non_bmp_map))
                    else:
                        reply = comment.reply("Hey there! Looks like you're not using our standard flair format which means I can't log your days. Send me a PM [here](https://www.reddit.com/message/compose/?to=1000DOP-Bot&subject=flair) with the contents being the emoji and days you want as part of your flair and I'll fix that for you! Make sure you don't request a flair with more days than you've already logged. Example: '\U0001F3B5 12'\n\nI am a bot and this action was performed automatically. Please contact [my creator](https://www.reddit.com/message/compose/?to=Dan6erbond&subject=1000DOP-Bot) if you have any questions or concerns.")
                        comment.mod.distinguish()
                        print("Replied to {}.".format(comment.author.name))

        except Exception as e:
            date_started = datetime.datetime.utcnow()
            print("{}: {}".format(type(e), e))
            sleep(3)
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

def get_template_id(day):
    template_id = "109a0770-23e3-11e9-82ff-0ed95a9c69a0"

    if day > 100:
        template_id = "bb98a602-1daf-11e9-8a1f-0e6585833b84"
    if day > 250:
        template_id = "d99048b8-1daf-11e9-ab91-0e314af13884"
    if day > 500:
        template_id = "f9c34270-1daf-11e9-bb22-0ee8915d3c24"
    if day > 750:
        template_id = "08c204b4-1db0-11e9-aae0-0eb3706cb7c0"
    if day == 1000:
        template_id = "29ff44fc-1db0-11e9-8f15-0ee0ed89fff4"
    if day > 1000:
        template_id = "b9629f32-1e68-11e9-942f-0e21fde54b6e"

    return template_id

'''
def reward(day):
    if day == 30:
        # send message
    if day == 50:
        # invite to Discord
    if day == 150:
        # send message
    if day == 182:
        # send message
    if day == 200:
        # send message
    if day == 250:
        # send message
        # create post
    if day == 300:
        # send message
    if day == 365:
        # send message
        # create post
    if day == 400:
        # send message
    if day == 450:
        # send message
    if day == 500:
        # send message
    if day == 550:
        # send message
        # create post
    if day == 600:
        # send message
    if day == 650:
        # send message
    if day == 700:
        # send message
    if day == 730:
        # send message
        # create post
    if day == 750:
        # send message
    if day == 800:
        # send message
    if day == 850:
        # send message
    if day == 912:
        # send message
        # create post
    if day == 950:
        # send message
    if day == 1000:
        # send message
        # create post
        # award gold
'''

read_comments()
