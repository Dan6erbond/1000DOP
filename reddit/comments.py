import praw
import sys
import re
from time import sleep
from datetime import datetime

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
    date_started = datetime.utcnow()
    while True:
        try:
            file = open("comments.txt")
            content = file.read()
            file.close()
            for comment in subreddit.stream.comments():
                in_daily_thread = "Daily" in comment.submission.link_flair_text if comment.submission.link_flair_text is not None else False
                parent_comment = "t3" in comment.parent_id

                if comment is not None and comment.author is not None and comment.id not in content and in_daily_thread and parent_comment: # and new:
                    print(comment.id)
                    flair = next(subreddit.flair(comment.author.name))["flair_text"]

                    if flair is None:
                        flair = ""

                    old_flair = flair

                    emojis = set()
                    for character in comment.body:
                        if character.encode('unicode-escape').decode('utf-8').lower().startswith("\\u"):
                            emojis.add(character)

                    highest_day = 0
                    partitions = flair.split("|")
                    for emoji in emojis:
                        for x in range(0,len(partitions)): # scan through the flair's partitions
                            if emoji in partitions[x]:
                                f = re.search("(\d+)", partitions[x])
                                days = 0 if not f else int(f.group(1)) + 1

                                if days > highest_day:
                                    highest_day = days
                                partitions[x] = "{} {} Day(s)".format(emoji, days)

                    partitions = [p.strip() for p in partitions]
                    flair = " | ".join(partitions)
                    
                    log = ""
                    if old_flair != flair:
                        template_id = get_template_id(highest_day)
                        subreddit.flair.set(comment.author, flair, flair_template_id=template_id)
                        log = "Replaced {} with {} for {}.".format(old_flair, flair, comment.author.name).translate(non_bmp_map)
                    else:
                        reply = comment.reply("Hey there! Looks like you're not using our standard flair format which means I can't log your days. Send me a PM [here](https://www.reddit.com/message/compose/?to=1000DOP-Bot&subject=flair) with the contents being the emoji and days you want as part of your flair and I'll fix that for you! Make sure you don't request a flair with more days than you've already logged. Example: '\U0001F3B5 12'\n\nI am a bot and this action was performed automatically. Please contact [my creator](https://www.reddit.com/message/compose/?to=Dan6erbond&subject=1000DOP-Bot) if you have any questions or concerns.")
                        reply.mod.distinguish()
                        log = "Replied to {}.".format(comment.author.name)
                        
                    with open("comments.txt", "a") as f:
                        f.write(comment.id + "\n")

                    print(log)
                    with open("log.txt", "a+", encoding="utf8") as f:
                        f.write(log + "\n")

        except ValueError as e:
            delta = datetime.utcnow() - date_started
            t = 3 if delta.seconds > 5 else 10
            date_started = datetime.utcnow()
            print("{}: {}".format(type(e), e))
            sleep(t)

def get_template_id(day):
    template_id = "109a0770-23e3-11e9-82ff-0ed95a9c69a0"

# new templates, changes every 20 days up to 1000 days
    if day > 20:
        template_id = "f24e4c96-626b-11e9-8e57-0ee9be4fc90e"
    if day > 40:
        template_id = "166e7920-626c-11e9-a103-0eec3f62b77c"
    if day > 60:
        template_id = "305d5b44-626c-11e9-8adc-0e2134b0c082"
    if day > 80:
        template_id = "3f851ada-626c-11e9-963b-0e48b74f8626"
    if day > 100:
        template_id = "510a7dfe-626c-11e9-b55f-0e27d1104956"
    if day > 120:
        template_id = "a3a2a8b6-626c-11e9-8168-0e26dcafe6e8"
    if day > 140:
        template_id = "b566af7a-626c-11e9-bd48-0ea5fb5d6588"
    if day > 160:
        template_id = "c8efbad2-626c-11e9-b5f9-0e24ce5715c4"
    if day > 180:
        template_id = "daa692b4-626c-11e9-96a2-0e24ce5715c4"
    if day > 200:
        template_id = "eff35e7c-626c-11e9-bf2b-0ebede5656ec"
    if day > 220:
        template_id = "a760114a-626d-11e9-aa4a-0e7a9c6b88d2"
    if day > 240:
        template_id = "b906293e-626d-11e9-9845-0e455eee425a"
    if day > 260:
        template_id = "c6f053ee-626d-11e9-9eeb-0e059e0c6668"
    if day > 280:
        template_id = "d339cef0-626d-11e9-9124-0ecea79423fa"
    if day > 300:
        template_id = "e2356194-626d-11e9-8c64-0e7cd917977e"
    if day > 320:
        template_id = "13809728-626e-11e9-8851-0e6b12138c22"
    if day > 340:
        template_id = "23bdd6f0-626e-11e9-be25-0ec83fb3c3c8"
    if day > 360:
        template_id = "30ac2fba-626e-11e9-b5f4-0e2e9a7f6762"
    if day > 380:
        template_id = "3c67aaa0-626e-11e9-ae63-0e918d6792d8"
    if day > 400:
        template_id = "48bbb1c0-626e-11e9-90ba-0efc74d5c2fe"
    if day > 420:
        template_id = "80135542-626e-11e9-bead-0e99dfb09b6a"
    if day > 440:
        template_id = "8df0c8f2-626e-11e9-a67f-0eab45bc0704"
    if day > 460:
        template_id = "99c86dba-626e-11e9-bbd3-0e1baf2d8a0a"
    if day > 480:
        template_id = "a63ab8b4-626e-11e9-aff0-0e71e991e91a"
    if day > 500:
        template_id = "b3e6430c-626e-11e9-bb33-0e096055fb6c"
    if day > 520:
        template_id = "c2e05626-626f-11e9-9b32-0e1bdebd9d3a"
    if day > 540:
        template_id = "d060ba48-626f-11e9-9fb3-0ee6aea24986"
    if day > 560:
        template_id = "37bf708a-6270-11e9-9aa5-0ed56b577244"
    if day > 580:
        template_id = "474dfcc4-6270-11e9-8f7b-0e99dfb09b6a"
    if day > 600:
        template_id = "54915020-6270-11e9-ad7c-0e4dc3f592fa"
    if day > 620:
        template_id = "7b830a34-6270-11e9-9e97-0e7f925c5d12"
    if day > 640:
        template_id = "89571b1e-6270-11e9-887f-0e7f80f038d8"
    if day > 660:
        template_id = "9505eb5c-6270-11e9-965a-0e607d9e7fcc"
    if day > 680:
        template_id = "a1fb479e-6270-11e9-a673-0e3f90a96136"
    if day > 700:
        template_id = "b1d64e20-6270-11e9-99f8-0e088ecbae30"
    if day > 720:
        template_id = "cc5d09f0-6270-11e9-bb33-0e096055fb6c"
    if day > 740:
        template_id = "d94d4080-6270-11e9-86e7-0eb536b4c774"
    if day > 760:
        template_id = "e551c90a-6270-11e9-83b1-0ef6e330c46e"
    if day > 800:
        template_id = "01c378ea-6271-11e9-a763-0e2cb77c8894"
    if day > 820:
        template_id = "3a9bb2fe-6271-11e9-a5ac-0eff4ce9f36c"
    if day > 840:
        template_id = "4cb82d28-6271-11e9-9601-0e72e4c65844"
    if day > 860:
        template_id = "59263424-6271-11e9-a30c-0e21ef4ee020"
    if day > 880:
        template_id = "6625e75a-6271-11e9-bea3-0e3bff7163b2"
    if day > 900:
        template_id = "7526631a-6271-11e9-9b39-0ee9be4fc90e"
    if day > 920:
        template_id = "cd223166-6271-11e9-a44c-0e3bff7163b2"
    if day > 940:
        template_id = "e184a30a-6271-11e9-b1b8-0ef861fe4132"
    if day > 960:
        template_id = "f590c57c-6271-11e9-970d-0e6abb8b6296"
    if day > 980:
        template_id = "051d164e-6272-11e9-8757-0ea5fb5d6588"
    if day > 1000:
        template_id = "194c574c-6272-11e9-8fd3-0ebecbde42d4"

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
