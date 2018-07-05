
import unittest
import flask
from .test_base import BaseTest

class TestEvidence(BaseTest):

    def test_1_first_message(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 1
                session['case'] = 2
            response = self.app.get('/evidence', data={'Body':'test'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_2_address(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 2
                session['case'] = 2
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/evidence', data={'Body':'120 North Ave NW Atlanta, GA'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    def test_3_chewed_or_droppings(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 3
                session['case'] = 2
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/evidence', data={'Body':'1'}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    def test_4_done(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 4
                session['case'] = 2
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/evidence', data={'Body':'Done', 'NumMedia': 0}, follow_redirects=True)
            print(response.data)
            self.assertEqual(response.status_code, 200)