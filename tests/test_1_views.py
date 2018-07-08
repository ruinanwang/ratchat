
import unittest
import flask
from .test_base import BaseTest

class TestViews(BaseTest):

    def test_1_web_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_2_message_retrieval(self):
        with self.app as app:
            response = app.get('/sms', data={'Body':'RAT'}, follow_redirects=True)
            self.assertEqual(flask.session['counter'], 1) 
            self.assertEqual(response.status_code, 200)
    
    def test_3_case_sighting(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
            response = self.app.get('/sms', data={'Body':'1'}, follow_redirects=True)
            self.assertIn('case', flask.session)
            self.assertEqual(response.status_code, 200)

    def test_4_case_evidence(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
            response = self.app.get('/sms', data={'Body':'2'}, follow_redirects=True)
            self.assertIn('case', flask.session)
            self.assertEqual(response.status_code, 200)

    def test_5_session_exists(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
                session['case'] = 1
            response = self.app.get('/sms', follow_redirects=True)
            self.assertIn('case', flask.session)
            self.assertIn('counter', flask.session)
            self.assertEqual(response.status_code, 200)

                  


