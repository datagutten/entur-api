import os
from unittest import TestCase

from entur_api.siri import Siri


class TestFindVehicleActivity(TestCase):
    siri = None
    file_path = None

    def setUp(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'test_data')
        self.siri = Siri('datagutten-tests', file=os.path.join(self.file_path, 'vm.xml'))
        pass

    def test_find(self):
        act = self.siri.find_vehicle_activity(
            origin_aimed_departure_time='2019-07-21T14:10:00+02:00',
            origin_quay='NSR:Quay:6263')
        self.assertEqual('Unibuss:8301:00810', act.block_ref())
        self.assertEqual('101130', act.vehicle())

    def test_find_with_line(self):
        act = self.siri.find_vehicle_activity(
            origin_aimed_departure_time='2019-07-21T14:10:00+02:00',
            origin_quay='NSR:Quay:6263',
            line='RUT:Line:83')
        self.assertEqual('Unibuss:8301:00810', act.block_ref())
        self.assertEqual('101130', act.vehicle())

    def test_find_with_line_and_quay(self):
        self.siri = Siri('datagutten-tests', file=os.path.join(self.file_path, 'vm_schedule.xml'))
        act = self.siri.find_vehicle_activity(
            origin_aimed_departure_time='2019-07-21T16:40:00+02:00',
            line='RUT:Line:83',
            origin_quay='NSR:Quay:6263')
        self.assertEqual('Unibuss:8302:00810', act.block_ref())
        self.assertEqual('101121', act.vehicle())

    def test_multiple(self):
        self.siri = Siri('datagutten-tests', file=os.path.join(self.file_path, 'vm-2020-01-18.xml'))
        act = self.siri.find_vehicle_activity(
            origin_aimed_departure_time='2020-01-18T10:10:00+01:00',
            line='RUT:Line:83',
            origin_quay='NSR:Quay:7216',
        )

        self.assertEqual('Unibuss:8101:2040', act.block_ref())
        self.assertEqual('103089', act.vehicle())

    def test_multiple_2(self):
        self.siri = Siri('datagutten-tests', file=os.path.join(self.file_path, 'vm-2020-01-18.xml'))
        act = self.siri.find_vehicle_activity(
            origin_aimed_departure_time='2020-01-18T09:42:00+01:00',
            line='RUT:Line:160',
            origin_quay='NSR:Quay:7724',
        )

        self.assertEqual('Norgesbuss:16006:2000', act.block_ref())
        self.assertEqual('328929', act.vehicle())

    def test_multiple_not_found(self):
        self.siri = Siri('datagutten-tests', file=os.path.join(self.file_path, 'vm-2020-01-18.xml'))
        act = self.siri.find_vehicle_activity(
            origin_aimed_departure_time='2020-01-18T12:40:00+01:00',
            line='RUT:Line:83',
            origin_quay='NSR:Quay:7216',
        )

        self.assertIsNone(act)
