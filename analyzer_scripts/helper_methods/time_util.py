from datetime import datetime


def convert_to_utc_time(t):
    dt_obj = datetime.utcfromtimestamp(t)

    return str(dt_obj)
