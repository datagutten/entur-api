from unittest import TestCase

from entur_api.siri import Siri


class SiriTest(TestCase):
    def test_vehicle_activities(self):
        siri = Siri('datagutten-entur-api-test', line='RUT:Line:83')
        activities = siri.vehicle_activities()
        self.assertIsNotNone(activities)
        for activity in activities:
            self.assertEqual('Unibuss', activity.operator())
            self.assertEqual('RUT:Line:83', activity.line_ref())
            self.assertEqual('83', activity.line_name())

    def test_location(self):
        siri = Siri('datagutten-entur-api-test', line='RUT:Line:83')
        activities = siri.vehicle_activities()
        for act in activities:
            pass
            # TODO: Find more stable tests
            # self.assertIsNotNone(act.previous_call()['StopPointRef'])
            # self.assertIsNotNone(act.onward_call()['StopPointRef'])
            # self.assertIsNotNone(act.monitored_call()['StopPointRef'])