import sqlite3


class sentiment_db:

    def __init__(self):
        self.conn = sqlite3.connect('sentiment_db.db')
        self.create_table() #creates the two database tables to store text comments

    def create_table(self):
        try:
            self.table_name_1 = 'comment_sentiment'
            self.table_name_2 = 'comment_atr'
            self.conn.execute('''CREATE TABLE ''' + self.table_name_1 + ''' 
            (com_ID text,Word text,Positive integer,Negative integer,Anger integer,Anticipation integer,Disgust integer,Fear integer,Joy integer,Sadness integer,Surprise integer,Trust integer)''')
            self.conn.execute('''CREATE TABLE ''' + self.table_name_2 + ''' 
            (com_ID text, user_id text, sub_id text , subred text)''')
            self.conn.commit()
        except:
            print ('table already exists!')

    def insert_row(self, target_row):
        #auto detect which table it should be inserted into
        if len(target_row[0]) > 4:
            self.conn.executemany(
                "insert into " + self.table_name_1 + "(com_ID,Word,Positive,Negative,Anger,Anticipation,Disgust,Fear,Joy,Sadness, Surprise,Trust) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                target_row)
        else:
            self.conn.executemany(
                "insert into " + self.table_name_2 + "(com_ID, user_id, sub_id, subred) "
                                                     "values (?, ?, ?, ?)",
            target_row)

        self.conn.commit()
