
import unittest
import flask
from .test_base import BaseTest

class TestMistakes(BaseTest):

    def test_1_sighting_mistake(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['case'] = 1
                session['counter'] = 1
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/mistakes', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_2_evidence_mistake(self):
        with self.app as app:
            with app.session_transaction() as session:                
                session['case'] = 2
                session['counter'] = 1
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/mistakes', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_3_general_mistake(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['case'] = None
            response = self.app.get('/mistakes', follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('case', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertNotIn('row_id', flask.session)
            self.assertEqual(response.status_code, 200)