import psycopg2
import sys

sys.path.insert(0, r'C:/Python Projects/reddit_mood_bot/')
from Creds.db import db_creds


def get_db_funct_object():
    try:
        connection = psycopg2.connect(user=db_creds['user'],
                                      password=db_creds['pw'],
                                      host=db_creds['host'],
                                      port="5432",
                                      database="reddit_mood")

        cursor = connection.cursor()
        print("Successfully logged into reddit_mood database")
        return [cursor, connection]

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        cursor.close()
        connection.close()


def close_connection(cursor, connection):
    cursor.close()
    connection.close()
