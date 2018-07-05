
import requests

class Geocoder(object):
    def __init__(self, key):
        self.url = 'https://maps.googleapis.com/maps/api/geocode/json'
        self.key = key

    def geocode(self, address):
        GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
        
        parameters = {
            'key': self.key,
            'address': address
        }

        request = requests.get(GOOGLE_MAPS_API_URL, params=parameters)
        response = request.json()
        result = response['results']

        if (result):
            lat = result[0]['geometry']['location']['lat']
            lon = result[0]['geometry']['location']['lng']
            address = result[0]['formatted_address']
            for item in result[0]['address_components']:
                if (item['long_name'] == 'Fulton County' or item['long_name'] == 'DeKalb County'):
                    return lat, lon, address
            return None, None, None
        else:
            return None, None, None