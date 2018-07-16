
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

            if query[:6] == "SELECT":
                self.records = []
                for (time, geocoded_address, lat, lon, report_type, out_in, dead_alive, chew_drop_hole) in cursor:
                    record = {}
                    record['time'] = time
                    record['address'] = geocoded_address
                    record['lat'] = lat
                    record['lon'] = lon
                    record['report_type'] = report_type
                    record['out_in'] = out_in
                    record['dead_alive'] = dead_alive
                    record['chew_drop_hole'] = chew_drop_hole
                    self.records.append(record)
            
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error:
            raise

    def get_row_id(self):
        return self.row_id
    
    def get_all_records(self):
        return self.records