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

    def get_first_payload_time(self):
        # TODO: (LOW) Write this more cleanly (hard)
        first_payload = {'size': '500',
                         'subreddit': self.subred_param,
                         'sort': self.sort_param}
        self.after_param, self.comment_latest_retrieval = time_util.get_last_response_time(first_payload)

    def get_first_payload(self):
        self.get_first_payload_time()
        self.size_param = '500'
        print('First time run through. Going back {}s'.format(self.after_param))
        return {'after': str(self.after_param) + 's',
                'size': self.size_param,
                'subreddit': self.subred_param,
                'sort': self.sort_param}

    def get_ongoing_payload(self):
        self.after_param = self.collection_timer()
        return {'after': str(self.after_param) + 's',
                'size': self.size_param,
                'subreddit': self.subred_param,
                'sort': self.sort_param}

    def collection_timer(self):
        diff_sec = int(time.time() - self.comment_latest_retrieval)
        if diff_sec <= 1:
            time.sleep(1)
            diff_sec = 1
        elif not self.comment_flag:
            time.sleep(1)
            diff_sec = math.ceil(diff_sec + 3)

        elif self.comment_flag:
            # self.get_first_payload_time()  # Reset the self.comment_latest_retrieval time
            diff_sec = int(time.time() - self.comment_latest_retrieval)
            self.comment_latest_retrieval += 10

        print('Collection Stream started on: {} || Current time: {} || Time since last collection: {}s'.format(
            time.strftime('%H:%M:%S', time.localtime(self.comment_latest_retrieval)),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            diff_sec))

        return diff_sec
