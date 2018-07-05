
from . import config, db_handler, geocoder
from flask import Flask

SECRET_KEY = config.secret_key
geocoder = geocoder.Geocoder(config.api_key)
db = db_handler.DB(config.db_credentials)
app = Flask(__name__)
app.config.from_object(__name__)
from . import views

if __name__ == '__main__':
    app.run()
