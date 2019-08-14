# TODO: Automatically detect and deploy the database tables
# TODO: Logging
import sys
sys.path.insert(0, 'C:/Python Projects/reddit_mood_bot')
import database_scripts.db_execution_objs as db_func
from database_scripts.queries.create_query import COMMENT_SENTIMENT, COMMENT_ATR
import psycopg2

def create_mood_table(cursor):
    cursor.execute(COMMENT_SENTIMENT)
    print ('Successfully created comment_sentiment table')

def create_comment_atr_table(cursor):
    cursor.execute(COMMENT_ATR)
    print ('Successfully created comment attribute table')

cursor, connection = db_func.get_db_funct_object()
create_mood_table(cursor)
create_comment_atr_table(cursor)
connection.commit()
db_func.close_connection(cursor,connection)

