
import unittest
import flask
from .test_base import BaseTest

class TestRestart(BaseTest):

    def test_1_sighting_restart(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['case'] = 1
                session['row_id'] = 1
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
                session['row_id'] = 1
            response = self.app.get('/sms/restart', follow_redirects=True)
            self.assertIn('counter', flask.session)
            self.assertNotIn('case', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertNotIn('row_id', flask.session)
            self.assertEqual(response.status_code, 200)
    
    def test_3_general_restart(self):
        response = self.app.get('/sms/restart', follow_redirects=True)
        self.assertEqual(response.status_code, 200)