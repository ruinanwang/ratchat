
import mysql.connector
from mysql.connector import errorcode

class DB(object):
    def __init__(self):
        self.row_id = 1
    
    def query(self, db_credentials, query, params=None):
        try:
            connection = mysql.connector.connect(**db_credentials)
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            if query[:6] == 'INSERT':
                self.row_id = cursor.lastrowid
            connection.close()
        except mysql.connector.Error:
            raise

    def getRowId(self):
        return self.row_id