import os
from unittest import TestCase

from entur_api.siri import Siri


class SiriTest(TestCase):
    file_path = None

    def setUp(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'test_data')

    def test_vehicle_activities(self):
        siri = Siri('datagutten-entur-api-test', line='RUT:Line:83')
        activities = siri.vehicle_activities()
        self.assertIsNotNone(activities)
        self.assertNotEqual(activities, [], 'List should not be empty')

        for activity in activities:
            self.assertEqual('Unibuss', activity.operator())
            self.assertEqual('RUT:Line:83', activity.line_ref())
            self.assertEqual('83', activity.line_name())

    def test_location(self):
        siri = Siri('datagutten-entur-api-test', file=os.path.join(self.file_path, 'vm.xml'))
        activities = siri.vehicle_activities()
        for act in activities:
            self.assertIsNotNone(act.previous_call()['StopPointRef'])
            self.assertIsNotNone(act.onward_call()['StopPointRef'])
            self.assertIsNotNone(act.monitored_call()['StopPointRef'])
