import psycopg2

def get_db_funct_object():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="hello123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="reddit_mood")
    
        cursor = connection.cursor()
        print ("Successfully logged into reddit_mood database")
        return [cursor, connection]
        
    except (Exception, psycopg2.Error) as error:
        print ("Error while connecting to PostgreSQL", error)
        cursor.close()
        connection.close()

def close_connection(cursor,connection):
    cursor.close()
    connection.close()
