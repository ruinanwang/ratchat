
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

    def test_0_geocode_response(self):
        lat, lon, address = self.geocoder.geocode('120 North Ave NW Atlanta, GA')
        self.assertNotEqual(lat, None)
        self.assertNotEqual(lon, None)
        self.assertNotEqual(address, None)

class Test2Views(TestBase):

    def test_1_web_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_2_message_retrieval(self):
        with self.app as app:
            response = app.post('/sms', data={'Body':'RAT'}, follow_redirects=True)
            self.assertEqual(flask.session['counter'], 1) 
            self.assertEqual(response.status_code, 200)
    
    def test_3_case_sighting(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
            response = self.app.post('/sms', data={'Body':'1'}, follow_redirects=True)
            self.assertIn('case', flask.session)
            self.assertEqual(response.status_code, 200)

    def test_4_case_evidence(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
            response = self.app.post('/sms', data={'Body':'2'}, follow_redirects=True)
            self.assertIn('case', flask.session)
            self.assertEqual(response.status_code, 200)

    def test_5_session_exists(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
                session['case'] = 1
            response = self.app.post('/sms', follow_redirects=True)
            self.assertIn('case', flask.session)
            self.assertIn('counter', flask.session)
            self.assertEqual(response.status_code, 200)

class Test3Evidence(TestBase):

    def test_1_first_message(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
                session['case'] = 2
            response = self.app.post('/sms/evidence', data={'Body':'test'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_2_address(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 2
                session['case'] = 2
                session['row_id'] = self.db.row_id
            response = self.app.post('/sms/evidence', data={'Body':'120 North Ave NW Atlanta, GA'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_3_chewed_or_droppings(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 3
                session['case'] = 2
                session['row_id'] = self.db.row_id
            response = self.app.post('/sms/evidence', data={'Body':'1'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_4_done(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 4
                session['case'] = 2
                session['row_id'] = self.db.row_id
            response = self.app.post('/sms/evidence', data={'Body':'Done', 'NumMedia': 0}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

class Test4Sighting(TestBase):

    def test_1_first_message(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
                session['case'] = 1
            response = self.app.post('/sms/sighting', data={'Body':'test'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_2_address(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 2
                session['case'] = 1
                session['row_id'] = self.db.row_id
            response = self.app.post('/sms/sighting', data={'Body':'120 North Ave NW Atlanta, GA'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_3_dead_or_alive(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 3
                session['case'] = 1
                session['row_id'] = self.db.row_id
            response = self.app.post('/sms/sighting', data={'Body':'1'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_4_inside_or_outside(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 4
                session['case'] = 1
                session['row_id'] = self.db.row_id
            response = self.app.post('/sms/sighting', data={'Body':'2'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_5_done(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 5
                session['case'] = 1
                session['row_id'] = self.db.row_id
            response = self.app.post('/sms/sighting', data={'Body':'Done', 'NumMedia': 0}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

class Test5Mistakes(TestBase):

    def test_1_sighting_mistake(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['case'] = 1
                session['counter'] = 1
                session['row_id'] = self.db.row_id
            response = self.app.get('/sms/mistakes', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_2_evidence_mistake(self):
        with self.app as app:
            with app.session_transaction() as session:                
                session['case'] = 2
                session['counter'] = 1
                session['row_id'] = self.db.row_id
            response = self.app.get('/sms/mistakes', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_3_general_mistake(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['case'] = None
            response = self.app.get('/sms/mistakes', follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('case', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertNotIn('row_id', flask.session)
            self.assertEqual(response.status_code, 200)

class Test6Restart(TestBase):

    def test_1_sighting_restart(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['case'] = 1
                session['row_id'] = self.db.row_id
            response = self.app.get('/sms/restart', follow_redirects=True)
            self.assertIn('counter', flask.session)
            self.assertNotIn('case', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertNotIn('row_id', flask.session)
            self.assertEqual(response.status_code, 200)

    def test_2_evidence_restart(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['case'] = 2
                session['row_id'] = self.db.row_id
            response = self.app.get('/sms/restart', follow_redirects=True)
            self.assertIn('counter', flask.session)
            self.assertNotIn('case', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertNotIn('row_id', flask.session)
            self.assertEqual(response.status_code, 200)
    
    def test_3_general_restart(self):
        response = self.app.get('/sms/restart', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

class Test7Info(TestBase):
    
    def test_1_info(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 2
                session['case'] = 2
                session['mistakes'] = 0
                session['row_id'] = self.db.row_id
            response = self.app.get('/sms/info', follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('case', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertNotIn('row_id', flask.session)
            self.assertEqual(response.status_code, 200)