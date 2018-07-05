
import unittest
import flask
from .test_base import BaseTest

class TestSighting(BaseTest):

    def test_1_first_message(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
                session['case'] = 1
            response = self.app.get('/sighting', data={'Body':'test'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_2_address(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 2
                session['case'] = 1
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/sighting', data={'Body':'120 North Ave NW Atlanta, GA'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_3_dead_or_alive(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 3
                session['case'] = 1
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/sighting', data={'Body':'1'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_4_inside_or_outside(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 4
                session['case'] = 1
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/sighting', data={'Body':'2'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_5_done(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 5
                session['case'] = 1
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/sighting', data={'Body':'Done', 'NumMedia': 0}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)