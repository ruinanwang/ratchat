
import unittest
import flask
from app import app, db, geocoder

class BaseTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SECRET_KEY'] = 'my2938secret0203key'
        self.geocoder = geocoder
        self.db = db
        self.app = app.test_client()