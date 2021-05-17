from unittest import TestCase

from entur_api import EnturJourneyPlanner as EnturApi, \
    EnturJourneyPlannerUtils as JourneyPlannerUtils


class EnturApiTests(TestCase):
    def test_get_departures(self):
        entur = EnturApi('datagutten-tests')
        departures = entur.stop_departures_app('NSR:StopPlace:58381')
        self.assertIsNotNone(departures)
        self.assertIn('estimatedCalls', departures['data']['stopPlace'])

    def test_filter(self):
        entur = JourneyPlannerUtils('datagutten-tests')
        departures = entur.filter_departures('NSR:StopPlace:58381',
                                             quays=['NSR:Quay:8027'])
        self.assertEqual('NSR:Quay:8027', departures[0]['quay']['id'])
        self.assertEqual('1', departures[0]['quay']['publicCode'])

    def test_filter_limit(self):
        entur = JourneyPlannerUtils('datagutten-tests')
        limit = 5
        departures = entur.filter_departures('NSR:StopPlace:58381',
                                             quays=['NSR:Quay:8027',
                                                    'NSR:Quay:8028'],
                                             limit=limit)

        self.assertEqual(len(departures), limit)

    def test_filter_none_limit(self):
        entur = JourneyPlannerUtils('datagutten-tests')
        departures = entur.filter_departures('NSR:StopPlace:58381',
                                             quays=['NSR:Quay:8027',
                                                    'NSR:Quay:8028'],
                                             limit=None)

        self.assertGreater(len(departures), 5)

    def test_stop_info(self):
        entur = EnturApi('datagutten-tests')
        stop_info = entur.stop_info('NSR:StopPlace:4483')
        self.assertEqual('Majorstuen',
                         stop_info['data']['stopPlace']['name'])
        # self.assertEqual('i Valkyriegata',
        #                  stop_info['data']['stopPlace']['description'])
        self.assertEqual('Majorstuen',
                         stop_info['data']['stopPlace']['quays'][0]['name'])

    def test_quay_description(self):
        entur = JourneyPlannerUtils('datagutten-tests')
        departures = entur.filter_departures('NSR:StopPlace:58381',
                                             quays=['NSR:Quay:8027'])
        self.assertEqual('Retning sentrum',
                         departures[0]['quay']['description'])
