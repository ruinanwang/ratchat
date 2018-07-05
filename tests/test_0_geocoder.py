
import unittest
import flask
from .test_base import BaseTest

class TestGeocoder(BaseTest):

    def test_1_first_message(self):
        lat, lon, address = self.geocoder.geocode('120 North Ave NW Atlanta, GA')
        self.assertNotEqual(lat, None)
        self.assertNotEqual(lon, None)
        self.assertNotEqual(address, None)