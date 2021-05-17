from unittest import TestCase

from entur_api.enturcommon import EnturCommon


class RequestTest(TestCase):
    def testCache(self):
        url = 'https://api.entur.io/realtime/v1/rest/vm?datasetId=RUT&' # &LineRef=RUT:Line:83&'
        entur = EnturCommon('datagutten-entur-api-test')
        self.assertEqual(entur.cache, {}, 'Cache should be empty')
        entur.rest_query(line_ref='RUT:Line:83', file_cache=False)  # Load data to cache
        time1 = entur.last_request
        self.assertIn(url, entur.cache, 'URL should be in cache')
        entur.rest_query(line_ref='RUT:Line:83', file_cache=False)  # Access data from cache
        time2 = entur.last_request
        self.assertEqual(time1, time2, 'Time should not change when caching')

    def testGetError(self):
        entur = EnturCommon('datagutten-entur-api-test')
        with self.assertRaises(Exception):
            entur.get('https://httpbin.org/status/429')
