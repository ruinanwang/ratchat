
# config_ex.py
# Example configuration file for RatWatch.

# Database credentials.
db_credentials = {
  'user': 'root',
  'password': 'root',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'database': 'ratwatch_db',
  'raise_on_warnings': False,  
}

# File path for image downloads.
image_directory = '/path/to/your/folder'

# Key for encrypting session cookies.
secret_key = 'secretkey'

# Key for accessing Google Maps Geocoding API.
api_key = 'api_key'

# SQL statements.
select_all_records = ("SELECT time, geocoded_address, lat, lon, report_type, out_in,"
                      + " dead_alive, chew_drop_hole FROM reports WHERE"
                      + " lat IS NOT NULL AND lon IS NOT NULL;")
insert_report = "INSERT INTO reports VALUES();"
update_image = "UPDATE reports SET image=%s WHERE id=%s;"
update_address = "UPDATE reports SET original_address=%s, geocoded_address=%s, lat=%s, lon=%s, geocoded=%s WHERE id=%s;"
update_sighting = "UPDATE reports SET report_type=%s, out_in=%s, dead_alive=%s, finished=%s WHERE id=%s;"
update_evidence = "UPDATE reports SET report_type=%s, chew_drop_hole=%s, finished=%s WHERE id=%s;"