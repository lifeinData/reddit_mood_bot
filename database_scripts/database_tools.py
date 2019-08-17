# TODO: delete the sys import method later on, only need to invoke it once

import sqlite3
import re

# Custom Imports
import sys
sys.path.insert(0, 'C:/Python Projects/reddit_mood_bot')
import database_scripts.db_execution_objs as db_func
import database_scripts.queries.analytics_query


class db_tools:

    def __init__(self):
        self.cursor, self.conn = db_func.get_db_funct_object()

    def insert_row(self, target_row):
        # auto detect which table it should be inserted into
        if len(target_row[0]) > 4:
            self.cursor.execute(
                """INSERT INTO COMMENT_SENTIMENT (com_ID,Word,Positive,Negative,Anger,Anticipation,Disgust,Fear,Joy,Sadness, Surprise,Trust) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                target_row[0])
        else:
            self.cursor.execute(
                """INSERT INTO COMMENT_ATR (com_ID, user_id, sub_id, subred) VALUES (%s, %s, %s, %s)""",
                target_row[0])

        self.conn.commit()

    def get_db_size(self, db_name):
        self.cursor.execute(
            """SELECT pg_size_pretty(pg_database_size(%s))""",
            (db_name,)
        )

        db_size = self.cursor.fetchall()
        return round (float(re.findall("\d+",str(db_size[0]))[0])/1000, 2)

