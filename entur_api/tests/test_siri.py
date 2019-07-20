from unittest import TestCase

from entur_api.siri import Activity, Siri


class SiriTest(TestCase):
    def test_vehicle_activities(self):
        siri = Siri(line='RUT:Line:83')
        activities = siri.vehicle_activities()
        self.assertIsNotNone(activities)
        for activity in activities:
            act = Activity(activity)
            self.assertEqual('Unibuss', act.operator())