# TODO: Logging
import pandas as pd
import re
import time
import requests
import math
from datetime import datetime

# Custom Packages
import sys

#TODO: use SYSPYTHON environment variable
sys.path.append(r'../../../reddit_mood_bot')
from Scripts.database.query_executors import database_tools as db_tools
from Scripts.redditBot_auth import bot_login
from Scripts.comment_analyzer.helper_methods import time_util
from Scripts.comment_analyzer.PayloadConfigs import PayloadConfigs
from Scripts.comment_analyzer.Logger_Messages.Stream_Msg import StreamMsg


class stream_analyzer():
    # TODO: df_sentiment_dict should be part of the database
    df_sentiment_dict = pd.read_excel(r'../../sentiment_dict.xlsx')
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
                t_row = [(self.com_id, self.user_id, self.sub_id, self.subred, self.datetime)]
                db_tools.insert_row(t_row)


# TODO: not 100% fidelity yet in terms of non-repeated comments, need to make that function
def comment_stream_reader():
    total_comments = 0
    restart = True
    first_run = True
    payload = PayloadConfigs()
    stream_logger = StreamMsg()
    while restart:

        payload_param = payload.get_payload()
        time.sleep(1)
        resp = requests.get('https://api.pushshift.io/reddit/search/comment/', params=payload_param)

        try:
            for data_point in resp.json()['data']:
                first_run = False
                comment_body = data_point['body'].split()
                stream_logger.append_subred_stats(resp.json()['data'][0]['subreddit'])

                if len(comment_body) < 600:
                    comment_time = time_util.convert_to_utc_time(data_point['created_utc'])
                    comment_subred = data_point['subreddit']
                    comment_author = data_point['author']
                    comment_id = data_point['id']
                    s_an = stream_analyzer(
                        comment_body, comment_subred, str(comment_id), comment_subred, comment_author, comment_time)
                    s_an.sentiment_analyzer()
        except:
            continue

        # TODO: Probably can write this in a cleaner way
        if not first_run:
            if len(resp.json()['data']) > 0:
                payload.set_comment_flag(True)
                stream_start_time = int(time.time())

                total_comments += len(resp.json()['data'])
                stream_logger.print_subreddit_count()
                print("DB Size: {} mb | Tot Comments: {} || Current Collection: {} in {}s".format(
                    db_tools.get_db_size("reddit_mood"), total_comments, len(resp.json()['data']),
                    payload.get_lag_time()))

            else:
                payload.set_comment_flag(False)

        if db_tools.db_full_check("reddit_mood", db_tools):  # Stop limit for database collection
            restart = False
            break

    # Things that should happen after all comments in this stream are analyzed


# TODO: Make post streaming stuff into class, there will be lots of stats and stuff for post streaming
reddit = bot_login.authenticate()
db_tools = db_tools.db_tools()
comment_stream_reader()
