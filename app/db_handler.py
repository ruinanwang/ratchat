
import mysql.connector
from mysql.connector import errorcode

class DB(object):
    def __init__(self, db_credentials):
        try:
            self.connection = mysql.connector.connect(**db_credentials)
            self.cursor = self.connection.cursor()
            self.row_id = 1
        except mysql.connector.Error:
            raise
    
    def query(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
        if query[:6] == 'INSERT':
            self.row_id = self.cursor.lastrowid
    
    def close(self):
        self.connection.close()

    def getRowId(self):
        return self.row_id