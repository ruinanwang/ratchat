
import unittest
import flask
import app.app, app.config, app.geocoder

class BaseTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SECRET_KEY'] = 'my2938secret0203key'
        self.geocoder = geocoder.Geocoder(config.api_key)
        self.app = app.test_client()