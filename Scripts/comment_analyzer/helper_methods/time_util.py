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
    for data_point in resp.json()['data']:
        return [int(time.time() - data_point['created_utc']), data_point['created_utc']]