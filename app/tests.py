
import unittest
import flask
from app import app, db, geocoder

class TestBase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SECRET_KEY'] = 'my2938secret0203key'
        self.db = db
        self.geocoder = geocoder
        self.app = app.test_client()

class Test1Geocoder(TestBase):

    def test_1_geocode_response(self):
        lat, lon, address = self.geocoder.geocode('120 North Ave NW Atlanta, GA')
        self.assertNotEqual(lat, None)
        self.assertNotEqual(lon, None)
        self.assertNotEqual(address, None)

class Test2Sms(TestBase):

    def test_1_web_page(self):
        with self.app as app:
            response = app.get('/', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_2_message_retrieval(self):
        with self.app as app:
            response = app.post('/sms', data={'Body':'RAT', 'NumMedia': 0}, follow_redirects=True)
            self.assertEqual(flask.session['counter'], 1) 
            self.assertEqual(response.status_code, 200)
    
    def test_3_image_retrieval(self):
        with self.app as app:
            response = app.post('/sms', data={'NumMedia': 1, 'MessageSid': 'test', 'MediaUrl0':'https://s3-external-1.amazonaws.com/media.twiliocdn.com/AC97a88511292ce1c17f84155aae5fdff5/45d0bd8624bc06dd74c042cd2fa3eff7'}, follow_redirects=True)
            self.assertEqual(flask.session['counter'], 1) 
            self.assertEqual(response.status_code, 200)

    def test_4_too_many_images(self):
        with self.app as app:
            response = app.post('/sms', data={'NumMedia': 2}, follow_redirects=True)
            self.assertNotIn('counter', flask.session) 
            self.assertEqual(response.status_code, 200)

class Test3Address(TestBase):

    def test_1_address(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['row_id'] = self.db.get_row_id()
            response = app.post('/sms/address', data={'Body':'120 North Ave NW Atlanta, GA'}, follow_redirects=True)
            self.assertEqual(flask.session['counter'], 2) 
            self.assertEqual(response.status_code, 200)

    def test_2_address_only_numbers(self):
        with self.app as app:
            response = app.post('/sms/address', data={'Body':'120'}, follow_redirects=True)
            self.assertNotIn('counter', flask.session) 
            self.assertEqual(response.status_code, 200)
    
    def test_3_address_only_letters(self):
        with self.app as app:
            response = app.post('/sms/address', data={'Body':'North Ave NW'}, follow_redirects=True)
            self.assertNotIn('counter', flask.session) 
            self.assertEqual(response.status_code, 200)

class Test4Options(TestBase):

    def test_1_outside_alive(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['row_id'] = self.db.get_row_id()
            response = app.post('/sms/options', data={'Body':'A'}, follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertEqual(response.status_code, 200)
    
    def test_2_inside_alive(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['row_id'] = self.db.get_row_id()
            response = app.post('/sms/options', data={'Body':'B'}, follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertEqual(response.status_code, 200)
    
    def test_3_outside_dead(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['row_id'] = self.db.get_row_id()
            response = app.post('/sms/options', data={'Body':'C'}, follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertEqual(response.status_code, 200)

    def test_4_inside_dead(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['row_id'] = self.db.get_row_id()
            response = app.post('/sms/options', data={'Body':'D'}, follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertEqual(response.status_code, 200)
    
    def test_5_chewed(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['row_id'] = self.db.get_row_id()
            response = app.post('/sms/options', data={'Body':'E'}, follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertEqual(response.status_code, 200)
    
    def test_6_droppings(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['row_id'] = self.db.get_row_id()
            response = app.post('/sms/options', data={'Body':'F'}, follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertEqual(response.status_code, 200)

    def test_7_hole(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['row_id'] = self.db.get_row_id()
            response = app.post('/sms/options', data={'Body':'G'}, follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertEqual(response.status_code, 200)