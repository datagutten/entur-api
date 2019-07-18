from unittest import TestCase

from entur_api.journey_planner import EnturApi
from entur_api.journey_planner_utils import JourneyPlannerUtils


class EnturApiTests(TestCase):
    def test_get_departures(self):
        entur = EnturApi('datagutten-tests')
        departures = entur.stop_departures_app('NSR:StopPlace:58381')
        self.assertIsNotNone(departures)
        self.assertEqual('Majorstuen', departures['data']['stopPlace']['name'])

    def test_filter(self):
        entur = JourneyPlannerUtils('datagutten-tests')
        departures = entur.filter_departures('NSR:StopPlace:58381',
                                             quays=['NSR:Quay:8027'])
        self.assertEqual('NSR:Quay:8027', departures[0]['quay']['id'])
        self.assertEqual('1', departures[0]['quay']['publicCode'])
