# TODO: Logging
import praw
import numpy
import pandas as pd
import re
import time

# Custom Packages
import sys
sys.path.insert(0, 'C:/Python Projects/reddit_mood_bot')
import database_scripts.database_tools as db_tools
import authentication_scripts.bot_login as bot_login

class stream_analyzer():

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

            #start = time.time()

                word = str(re.findall('[A-Za-z]+', word))[2:-2]
                if (word.lower() in stream_analyzer.word_l) == True:
                    self.total_word_stream_hit += 1
                    t_row = stream_analyzer.df_sentiment_dict[stream_analyzer.df_sentiment_dict['Word'] == word.lower()].values.tolist()
                    t_row[0].insert(0, self.com_id)
                    db_tools.insert_row(t_row)
        
                    if self.total_word_stream_hit > 1:
                        t_row = [(self.com_id, self.user_id, self.sub_id, self.subred)]
                        db_tools.insert_row(t_row)


def comment_stream_reader():
    n = 0
    
    restart = True
    while restart:
        cs = reddit.subreddit('depression').stream.comments()
        start = time.time()
        for comment in cs:
            n += 1
            body = comment.body.split()
            print (n)

            if ((time.time() - start) > 10):
                print ('Restarting the comment stream')
                break

            if len(body) < 50 and 'http' not in body:
                sub_id = comment.submission.id
                subred = comment.subreddit.display_name
                user_id = comment.author.name
                s_an = stream_analyzer(
                    body, sub_id, str(comment.id), subred, user_id)
                s_an.sentiment_analyzer()

            if (n % 100) == 0:
                print ('time taken for 100 comments: {}'.format (time.time() - start))
                print ('read 100 comments')
                print ("Current memory taken is: {} mb".format(db_tools.get_db_size("reddit_mood")))
                start = time.time()
            
            elif db_tools.get_db_size("reddit_mood") > 100:
                restart = False
                break

reddit = bot_login.authenticate()
db_tools = db_tools.db_tools()
comment_stream_reader()
