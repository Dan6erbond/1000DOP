import praw
import datetime
import sys
# from requests.exceptions import ConnectionError, HTTPError
from time import sleep

reddit = praw.Reddit("1000DOP")
subreddit = reddit.subreddit("1000DaysOfPractice")

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def edit_wiki():
    try:
        page = subreddit.wiki["halloffame"]
        content = page.content_md
        content = """#Hall of Fame

---
User|Achievement
:--|:--
User1|Achievement1
User2|Achievement2"""
        page.edit(content)
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

edit_wiki()
