# TODO: delete the sys import method later on, only need to invoke it once

import re

# Custom Imports
import sys

sys.path.insert(0, r'C:/Python Projects/reddit_mood_bot')
from Scripts.database.query_executors import db_execution_objs as db_func


class db_tools:

    def __init__(self):
        self.cursor, self.conn = db_func.get_db_funct_object()

    def insert_row(self, target_row):
        # TODO: Insert query_statements should be part of the query_statements directory
        # TODO: A better way to auto detect which table it should be inserted into
        if len(target_row[0]) > 5:
            self.cursor.execute(
                """INSERT INTO comment_sentiment (com_id, word, positive, negative, anger, anticipation, disgust, fear, joy, sadness, surprise, trust) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                target_row[0])
        else:
            self.cursor.execute(
                """INSERT INTO COMMENT_ATR (com_id, user_id, sub_id, subred, comment_time) VALUES (%s, %s, %s, %s, %s)""",
                target_row[0])

        self.conn.commit()

    def get_db_size(self, db_name):
        self.cursor.execute(
            """SELECT pg_database_size(%s)""",
            (db_name,)
        )
        db_size = self.cursor.fetchall()
        return round(float(re.findall("\d+", str(db_size[0]))[0]) / 1000000, 2)

    def db_full_check(self, db_name, db_obj):
        # TODO: parameterize
        if db_obj.get_db_size(db_name) > 1000:
            return True

        return False

# TODO: Need to make sure that database only contains unique until we figure out a way to get 100% unique comments on collection step
