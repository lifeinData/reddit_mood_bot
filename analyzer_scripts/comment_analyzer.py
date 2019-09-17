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
import analyzer_scripts.helper_methods.time_util as time_util


class stream_analyzer():
    # TODO: df_sentiment_dict should be part of the database
    df_sentiment_dict = pd.read_excel(r'C:\Python Projects\reddit_mood_bot\sentiment_dict.xlsx')
    word_l = df_sentiment_dict['Word'].tolist()
    print('Sentiment dicitonary loaded')

    def __init__(self, comment, sub_id, com_id, subred, user_id, comment_time):

        self.word_stream = comment
        self.sub_id = sub_id
        self.com_id = com_id
        self.subred = subred
        self.user_id = user_id
        self.datetime = comment_time
        self.sentiment = None
        self.total_word_stream_count = len(comment)
        self.total_word_stream_hit = 0

    def sentiment_analyzer(self):
        for word in self.word_stream:
            try:
                word = str(re.findall('[A-Za-z]+', word)[0])
            except IndexError:
                pass

            if word.lower() in stream_analyzer.word_l:
                # The actual sentiment of the word that is a hit
                self.total_word_stream_hit += 1
                t_row = stream_analyzer.df_sentiment_dict[
                    stream_analyzer.df_sentiment_dict['Word'] == word.lower()].values.tolist()
                t_row[0].insert(0, self.com_id)
                db_tools.insert_row(t_row)

                # Insert meta data on the comment
                t_row = [(self.com_id, self.user_id, self.sub_id, self.subred)]
                db_tools.insert_row(t_row)


# TODO: not 100% fidelity yet in terms of non-repeated comments, need to make that function
def comment_stream_reader():
    total_comments = 0
    restart = True
    first_run = True
    stream_start_time = None

    while restart:
        try:
            # TODO: (LOW) parameter constants
            payload_time = get_dynamic_seconds(stream_start_time)
            payload_subred = ['Depression,news,worldnews,Happy']
            payload = {'after': payload_time, 'size': '500',
                       'subreddit': payload_subred,
                       'sort': 'desc'}
            resp = requests.get('https://api.pushshift.io/reddit/search/comment/', params=payload)

            for data_point in resp.json()['data']:
                first_run = False
                comment_body = data_point['body'].split()
                print(resp.json()['data'][0]['subreddit'])
                if len(comment_body) < 600 and 'http' not in comment_body:
                    comment_time = time_util.convert_to_utc_time(data_point['created_utc'])
                    comment_subred = data_point['subreddit']
                    comment_author = data_point['author']
                    comment_id = data_point['id']
                    s_an = stream_analyzer(
                        comment_body, comment_subred, str(comment_id), comment_subred, comment_author, comment_time)
                    s_an.sentiment_analyzer()

            # TODO: Probably can write this in a cleaner way
            if not first_run:
                if len(resp.json()['data']) > 0:
                    stream_start_time = int(time.time())
                    total_comments += len(resp.json()['data'])
                    print("DB Size: {} mb | Tot Comments: {} || Current Collect: {} in {} ".format(
                        db_tools.get_db_size("reddit_mood"), total_comments, len(resp.json()['data']), payload_time))

            if db_tools.db_full_check("reddit_mood", db_tools):  # Stop limit for database collection
                restart = False
                break

        except:
            pass

            # Things that should happen after all comments in this stream are analyzed


# TODO: Make post streaming stuff into class, there will be lots of stats and stuff for post streaming

def get_dynamic_seconds(previous_time=None):
    # previous_time is when the last time the response had data unless it's the first run
    if previous_time is None:
        print('First time run through. Going back 300s')
        return '300s'

    else:
        diff_sec = int(time.time()) - previous_time
        print('Collection Stream started on: {} || Current time: {} || Time since last collection: {}s'.format(
            time.strftime('%H:%M:%S', time.localtime(previous_time)), datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            diff_sec))

        if diff_sec <= 1:
            time.sleep(1)
            diff_sec = 1
        else:
            time.sleep(1)
            diff_sec = math.ceil(diff_sec + 1)

    return str(diff_sec) + 's'


reddit = bot_login.authenticate()
db_tools = db_tools.db_tools()
comment_stream_reader()
