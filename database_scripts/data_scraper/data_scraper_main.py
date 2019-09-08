import requests
import time
import datetime
import math
import pandas as pd

run_scraper = True
current_epoch = None
time_list = []
first_run = True
n = 0


def get_dynamic_seconds(start_time=None):
    if start_time is None:
        print('used the default one!')
        return '300s'
    else:
        now_time = int(time.time())
        # start_time is when the last time the response had data
        diff_sec = int(time.time()) - start_time

        if diff_sec <= 1:
            time.sleep(1)
            diff_sec = 1
        else:
            time.sleep(1)
            diff_sec = math.ceil(diff_sec + 1)

        print(str(diff_sec) + 's')
        return str(diff_sec) + 's'


while run_scraper:
    payload = {'after': get_dynamic_seconds(current_epoch), 'size': '500', 'subreddit': 'AskReddit', 'sort': 'desc'}

    if first_run:
        current_epoch = int(time.time())

    resp = requests.get('https://api.pushshift.io/reddit/search/comment/', params=payload)
    # might loss some comments based on speed of processing here (between getting resp and the next int(time.time()))

    print('# of comments: {} ||| Elasped time: {}'.format(len(resp.json()['data']), int(time.time()) - current_epoch))

    if len(resp.json()['data']) > 1 and first_run == False:
        print('rest current time counter')
        current_epoch = int(time.time())

    for d in resp.json()['data']:
        print(
            'comment time {} in {}'.format(time.strftime('%H:%M:%S', time.localtime(d['created_utc'])), d['subreddit']))
        #         print ('seconds since last comment {}'.format(int(curent_epoch - d['created_utc'])), time.strftime('%H:%M:%S:%f', time.localtime(d['created_utc'])))
        time_list.append(d['id'])
        n += 1

    if n > 1:
        first_run = False
    elif n > 10000:
        run_scraper = False
