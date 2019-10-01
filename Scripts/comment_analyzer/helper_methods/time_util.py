from datetime import datetime
import requests
import time

def convert_to_utc_time(t):
    dt_obj = datetime.utcfromtimestamp(t)

    return str(dt_obj)


def get_last_response_time(payload):
    # Determines the "After" Parameter time if pushshift is lagging
    resp = requests.get('https://api.pushshift.io/reddit/search/comment/', params=payload)
    payload['sort'] = 'asc'
    # resp2 = requests.get('https://api.pushshift.io/reddit/search/comment/', params=payload)
    time_list = [data_point['created_utc'] for data_point in resp.json()['data']]
    for data_point in resp.json()['data']:
        return [int(data_point['retrieved_on'] - data_point['created_utc']) + 10, data_point['created_utc']]