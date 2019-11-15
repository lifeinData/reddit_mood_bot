from Scripts.comment_analyzer.helper_methods import time_util
import time
import math
from datetime import datetime


class PayloadConfigs():
    def __init__(self):
        # Some have default settings
        self.after_param = None
        self.before_param = None
        self.size_param = None
        self.sort_param = 'desc'
        self.subred_param = ['Depression,news,worldnews,Happy']  # TODO: (LOW) Make subreddits into a constant
        self.comment_latest_retrieval = None
        self.first_run = True
        self.payload_timer = None
        self.comment_flag = None

    def set_comment_flag(self, flag_bool):
        self.comment_flag = flag_bool

    def get_payload(self):
        # Control method of which payload to get (first time or continous)
        if self.first_run:
            self.first_run = False
            return self.get_first_payload()

        else:
            return self.get_ongoing_payload()

    def get_first_payload(self):

        self.get_first_payload_time()  # retrieves the first intance where there is a comment
        self.size_param = '500'
        print('First time run through. Going back {}s'.format(self.after_param))
        return {'after': str(self.after_param) + 's',
                'size': self.size_param,
                'subreddit': self.subred_param,
                'sort': self.sort_param}

    def get_first_payload_time(self):
        # TODO: (LOW) Write this more cleanly (hard)
        # Gets the lag time (aka after_param) and the time since epoch of the first comment retrieved since this stream started
        size_param = '1'
        first_payload = {'size': size_param,
                         'subreddit': self.subred_param,
                         'sort': self.sort_param}

        self.after_param, self.comment_latest_retrieval = time_util.get_last_response_time(first_payload)

    def get_ongoing_payload(self):
        self.after_param = self.collection_timer()
        self.size_param = '500'
        return {'after': str(self.after_param) + 's',
                'size': self.size_param,
                'subreddit': self.subred_param,
                'sort': self.sort_param}

    def collection_timer(self):

        diff_sec = int(
            time.time() - self.comment_latest_retrieval + 1)  # adding 1 second will counter any chance of reoccuring comment

        lag_reset_flag = False

        # TODO: make into rest end points
        print('Current time: {} || Time of last positive stream: {}s || Lag time: {}s || Lag Reset: {}'.format(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            time.strftime('%H:%M:%S', time.localtime(self.comment_latest_retrieval)),
            self.after_param,
            str(lag_reset_flag)))

        if diff_sec <= 1:
            time.sleep(1)
            diff_sec = 1

        elif not self.comment_flag:
            # increase the after param if there is no hit
            time.sleep(2)
            diff_sec = math.ceil(diff_sec + 2)
            prev_latest_time = self.comment_latest_retrieval
            self.comment_latest_retrieval, lag_reset_flag = self.check_latest_lag(prev_latest_time)

            if self.comment_latest_retrieval > prev_latest_time:
                diff_sec = int(time.time() - self.comment_latest_retrieval + 1)

            return diff_sec

        elif self.comment_flag:
            # self.get_first_payload_time()  # Reset the self.comment_latest_retrieval time
            # Use the same length time as the previous after parameter
            time.sleep(2)
            # TODO: think about the dynamic lag portion
            return self.after_param - 2
            # diff_sec = int(time.time() - self.comment_latest_retrieval)
            # self.comment_latest_retrieval += 10

    def check_latest_lag(self, last_retrieval):
        # Determines if the lag is x% better than previous retrieval time
        faster, slower = 0, 0
        self.get_first_payload_time()
        tmp_lastest_time = self.comment_latest_retrieval
        prct_better_lag = 0.1
        # if last_retrieval > round((1 + prct_better_lag) * tmp_lastest_time, 0):
        if tmp_lastest_time > last_retrieval:
            faster += 1
            print('faster times:', faster)
            return [tmp_lastest_time, True]

        elif last_retrieval > tmp_lastest_time:
            slower += 1
            print('slower times:', slower)
            return [last_retrieval, True]

        else:
            return [last_retrieval, False]

    def get_lag_time(self):
        return self.after_param
