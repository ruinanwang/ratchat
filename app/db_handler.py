
import mysql.connector
from mysql.connector import errorcode

class DB(object):
    def __init__(self):
        self.row_id = 1
        self.records = []

    def execute(self, db_credentials, query, params=None):
        try:
            connection = mysql.connector.connect(**db_credentials)
            cursor = connection.cursor()
            cursor.execute(query, params)

            if query[:6] == "INSERT":
                self.row_id = cursor.lastrowid
            
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error:
            raise

    def get_row_id(self):
        return self.row_id