
import unittest
import flask
from .test_base import BaseTest

class TestInfo(BaseTest):
    
    def test_1_info(self):
        with self.app as app:
            with app.session_transaction() as session:
                session['counter'] = 2
                session['case'] = 2
                session['mistakes'] = 0
                session['row_id'] = self.db.getRowId()
            response = self.app.get('/info', follow_redirects=True)
            self.assertNotIn('counter', flask.session)
            self.assertNotIn('case', flask.session)
            self.assertNotIn('mistakes', flask.session)
            self.assertNotIn('row_id', flask.session)
            self.assertEqual(response.status_code, 200)
