import bot_script.bot_login as bot_login
import bot_script.database_tools as db_t
import praw
import numpy
import pandas as pd
import re
from autocorrect import spell
import time


class stream_analyzer():

    df_sentiment_dict = pd.read_excel('sentiment_dict.xlsx')
    word_l = df_sentiment_dict['Word'].tolist()
    print ('Sentiment dicitonary loaded')

    def __init__ (self, comment, sub_id, com_id, subred, user_id):

        self.word_stream = comment
        self.sub_id = sub_id
        self.com_id = com_id
        self.subred = subred
        self.user_id = user_id
        self.sentiment = None

    def sentiment_analyzer (self):
        for word in self.word_stream:
            print('processing the following word: {}'.format(word))
            #start = time.time()
            if 'http' not in word:
                word = spell(str(re.findall('[A-Za-z]+', word))[2:-2]).lower()

            if (word in stream_analyzer.word_l) == True:
                print ('The following word was processed: {}'.format(word))
                t_row = stream_analyzer.df_sentiment_dict[stream_analyzer.df_sentiment_dict['Word'] == word].values.tolist()
                t_row[0].insert(0, self.com_id)
                db_tools.insert_row(t_row)
                print('The following word was inserted into the data base: {}'.format(word))

        t_row = [(self.com_id, self.user_id, self.sub_id, self.subred)]
        db_tools.insert_row(t_row)
        #print('timetaken per comment : {}'.format(time.time() - start))

def comment_stream_reader (cs):
    n = 0
    for comment in cs:
        start = time.time()
        body = comment.body.split()
        # if len(body) < 50:
        #     sub_id = comment.submission.id
        #     subred = comment.subreddit.display_name
        #     user_id = comment.author.name
            # s_an = stream_analyzer(body,sub_id,str(comment.id),subred, user_id)
            # s_an.sentiment_analyzer()

        n +=1

        if (n%100) == 0:
            return ([time.time(), start])
            #return ('time taken for 100 comments: {}'.format (time.time() - start))
            #return ('read 100 comments')

reddit = bot_login.authenticate()
db_tools = db_t.sentiment_db()


while True:
    comment_stream = reddit.subreddit('all').stream.comments()
    print (comment_stream_reader(comment_stream)[0]-comment_stream_reader(comment_stream)[1])



