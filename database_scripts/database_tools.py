# TODO: delete the sys import method later on, only need to invoke it once
import database_scripts.db_execution_objs as db_func
import sqlite3
import sys
sys.path.insert(0, 'C:/Python Projects/reddit_mood_bot')


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
