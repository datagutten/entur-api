from unittest import TestCase

from entur_api import GeoCoder


class GeoCodeTest(TestCase):
    def setUp(self):
        self.geocoder = GeoCoder('datagutten-test')

    def test_reverse_lookup(self):
        stops = self.geocoder.reverse('59.807217', '10.796117')
        properties = stops[0]['properties']
        self.assertEqual('NSR:StopPlace:3401', properties['id'])
        self.assertEqual('Ingierkollveien', properties['name'])
