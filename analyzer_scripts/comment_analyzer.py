# TODO: Logging
import praw
import numpy
import pandas as pd
import re
import time
import requests
import math
from datetime import datetime


# Custom Packages
import sys
sys.path.insert(0, 'C:/Python Projects/reddit_mood_bot')
import database_scripts.database_tools as db_tools
import authentication_scripts.bot_login as bot_login

class stream_analyzer():
    #TODO: df_sentiment_dict should be part of the database
    df_sentiment_dict = pd.read_excel('sentiment_dict.xlsx')
    word_l = df_sentiment_dict['Word'].tolist()
    print('Sentiment dicitonary loaded')

    def __init__(self, comment, sub_id, com_id, subred, user_id):

        self.word_stream = comment
        self.sub_id = sub_id
        self.com_id = com_id
        self.subred = subred
        self.user_id = user_id
        self.sentiment = None
        self.total_word_stream_count = len(comment)
        self.total_word_stream_hit = 0

    def sentiment_analyzer(self):
        for word in self.word_stream:
            try:
                word = str(re.findall('[A-Za-z]+', word)[0])
            except IndexError:
                pass

            if (word.lower() in stream_analyzer.word_l) == True:
                # The actual sentiment of the word that is a hit
                self.total_word_stream_hit += 1
                t_row = stream_analyzer.df_sentiment_dict[stream_analyzer.df_sentiment_dict['Word'] == word.lower()].values.tolist()
                t_row[0].insert(0, self.com_id)
                db_tools.insert_row(t_row)

                # Insert meta data on the comment
                t_row = [(self.com_id, self.user_id, self.sub_id, self.subred)]
                db_tools.insert_row(t_row)


# TODO: not 100% fidelity yet in terms of non-repeated comments, need to make that function
def comment_stream_reader():
    n = 0
    restart = True
    first_run = True
    stream_start_time = None

    while restart:
        payload = {'after': get_dynamic_seconds(stream_start_time), 'size':'500', 'subreddit':'AskReddit', 'sort':'desc'}
        
        # TODO: Probably can write this in a cleaner way
        if first_run == False: 
            if len(resp.json()['data']) > 0:
                stream_start_time = int(time.time())
                n += len(resp.json()['data'])
                print ("Current memory taken is: {} mb after {} comments in this current run".format(db_tools.get_db_size("reddit_mood"),n))

        resp = requests.get('https://api.pushshift.io/reddit/search/comment/', params = payload)
        for data_point in resp.json()['data']:
            first_run = False
            comment_body = data_point['body'].split()

            if len(comment_body) < 50 and 'http' not in comment_body:
                comment_subred = data_point['subreddit']
                comment_author = data_point['author']
                comment_id = data_point['id']
                s_an = stream_analyzer(
                    comment_body, comment_subred, str(comment_id), comment_subred, comment_author)
                s_an.sentiment_analyzer()
        
        
        if db_tools.get_db_size("reddit_mood") > 100:
                restart = False
                break
                
        # Things that should happen after all comments in this stream are analyzed

# TODO: Make post streaming stuff into class, there will be lots of stats and stuff for post streaming

# def post_stream_processing():
# db_tools.get_db_size("reddit_mood") > 100:
    #             restart = False
    #             break

def get_dynamic_seconds(previous_time = None):
    if previous_time is None:
        print ('first time run through') 
        return '300s'
    else:
        print ('The stream started to analyze the comments on {}, now is: {} '.format(time.strftime('%H:%M:%S', time.localtime(previous_time)), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        now_time = int(time.time())
        # start_time is when the last time the response had data
        diff_sec = int(time.time()) - previous_time

        if diff_sec <= 1:
            time.sleep(1)
            diff_sec = 1
        else:
            time.sleep(1)
            diff_sec = math.ceil(diff_sec + 1)
            
        print (str(diff_sec) + 's')

    return str(diff_sec) + 's'
    # while restart:
    #     cs = reddit.subreddit('depression').stream.comments()
    #     start = time.time()
    #     for comment in cs:
    #         n += 1
    #         body = comment.body.split()
    #         print (n)

    #         if ((time.time() - start) > 10):
    #             print ('Restarting the comment stream')
    #             break

    #         if len(body) < 50 and 'http' not in body:
    #             sub_id = comment.submission.id
    #             subred = comment.subreddit.display_name
    #             user_id = comment.author.name
    #             s_an = stream_analyzer(
    #                 body, sub_id, str(comment.id), subred, user_id)
    #             s_an.sentiment_analyzer()

    #         if (n % 100) == 0:
    #             print ('time taken for 100 comments: {}'.format (time.time() - start))
    #             print ('read 100 comments')
    #             print ("Current memory taken is: {} mb".format(db_tools.get_db_size("reddit_mood")))
    #             start = time.time()
            
    #         elif db_tools.get_db_size("reddit_mood") > 100:
    #             restart = False
    #             break

reddit = bot_login.authenticate()
db_tools = db_tools.db_tools()
comment_stream_reader()
