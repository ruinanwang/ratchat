
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
insert_report_original = "INSERT INTO original_reports VALUES();"
update_image_original = "UPDATE original_reports SET image=%s WHERE id=%s;"
update_address_original = "UPDATE original_reports SET address=%s, lat=%s, lon=%s WHERE id=%s;"
update_sighting_original = "UPDATE original_reports SET type=%s, out_in=%s, dead_alive=%s, finished=%s WHERE id=%s;"
update_evidence_original = "UPDATE original_reports SET type=%s, chew_drop_hole=%s, finished=%s WHERE id=%s;"

insert_report_altered = "INSERT INTO altered_reports VALUES();"
update_image_altered = "UPDATE altered_reports SET image=%s WHERE id=%s;"
update_address_altered = "UPDATE altered_reports SET address=%s, lat=%s, lon=%s WHERE id=%s;"
update_sighting_altered = "UPDATE altered_reports SET type=%s, out_in=%s, dead_alive=%s, finished=%s WHERE id=%s;"
update_evidence_altered = "UPDATE altered_reports SET type=%s, chew_drop_hole=%s, finished=%s WHERE id=%s;"