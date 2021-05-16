from xml.etree import ElementTree

from entur_api.Activity import Activity
from .enturcommon import EnturCommon


class Siri(EnturCommon):

    namespaces = {'siri': 'http://www.siri.org.uk/siri'}
    tree = None
    line = None

    def __init__(self, client, line=None, file=None, operator='RUT'):
        super().__init__(client)

        # print(line)
        if line:
            xml_string = self.rest_query(line_ref=line)
            self.line = line
        elif file:
            f = open(file, 'r')
            xml_string = f.read()
            f.close()
        elif operator:
            xml_string = self.rest_query(operator=operator)
        else:
            raise Exception('file or line must be specified')

        self.tree = ElementTree.fromstring(xml_string)

    def vehicle_activities(self):
        if self.line:
            activities_xml = self.tree.findall(
                './/siri:VehicleMonitoringDelivery/siri:VehicleActivity/siri:MonitoredVehicleJourney/siri:LineRef[.="%s"]/../..' % self.line,
                self.namespaces)
        else:
            activities_xml = self.tree.findall(
                './/siri:VehicleMonitoringDelivery/siri:VehicleActivity', self.namespaces)
        activities = []
        for activity_xml in activities_xml:
            activities.append(Activity(activity_xml))

        return activities

    def get_vehicle_activity(self, vehicle_id):
        q = './/siri:VehicleMonitoringDelivery/siri:VehicleActivity/siri:MonitoredVehicleJourney[siri:VehicleRef="%s"]/..'
        act = self.tree.find(q % vehicle_id, self.namespaces)
        if act:
            return Activity(act)

    def find_vehicle_activity(self, origin_aimed_departure_time=None,
                              origin_quay=None, line=None, debug=False):
        q = './/siri:VehicleMonitoringDelivery'
        act = self.tree.find(q, self.namespaces)
        acts = []
        if debug:
            print(origin_aimed_departure_time)
        if origin_aimed_departure_time:
            acts = act.findall('.//siri:OriginAimedDepartureTime[.="%s"]/../..' %
                               origin_aimed_departure_time, self.namespaces)
            if not acts:
                return

            if debug:
                print('%d OriginAimedDepartureTime found' % len(acts))
                print('origin_aimed_departure_time', origin_aimed_departure_time, acts[0])
                activity = Activity(acts[0])
                print('Line', activity.line_ref())

        if origin_quay:
            acts_tmp = []
            if not acts:
                acts = act.findall('.//siri:OriginRef[.="%s"]/../..' % origin_quay,
                                   self.namespaces)
                if not acts:
                    return
            else:
                for act in acts:
                    activity = Activity(act)
                    if activity.origin_ref() == origin_quay:
                        acts_tmp.append(act)
                acts = acts_tmp
            if debug:
                print('origin_quay', origin_quay, act)
        if line:
            acts_tmp = []
            if not acts:
                acts = act.findall('.//siri:LineRef[.="%s"]/../..' % line,
                                   self.namespaces)
                if not acts:
                    return
            else:
                for act in acts:
                    activity = Activity(act)
                    if activity.line_ref() == line:
                        acts_tmp.append(act)

                if debug:
                    print('line', line, act)
                acts = acts_tmp

        if acts is not None:
            if len(acts) == 1:
                return Activity(acts[0])
            else:
                raise Exception('Multiple activities found, add more filters')

    def journey(self, journey=None, departure=None, arrival=None, quay=None):
        if journey:
            q = './/siri:FramedVehicleJourneyRef/siri:DatedVehicleJourneyRef[.="%s"]' % journey
            q += '/../../..'
            q_check = './/siri:FramedVehicleJourneyRef/siri:DatedVehicleJourneyRef'
            value = journey
        elif arrival:
            q = './/siri:DestinationAimedArrivalTime[.="%s"]' % arrival
            if quay:
                q += '/../siri:DestinationRef[.="%s"]' % quay
            q += '/../..'
            q_check = './/siri:DestinationAimedArrivalTime'
            value = arrival
        elif departure:
            q = './/siri:OriginAimedDepartureTime[.="%s"]' % departure
            q += '/../..'
            q_check = './/siri:OriginAimedDepartureTime'
            value = departure
        else:
            raise Exception('Missing argument')

        try:
            act = self.tree.find(q, self.namespaces)
        except SyntaxError:
            act = None
        if act is None:
            print('Could not find %s' % value)
            print('Valid values:')
            for item in self.tree.findall(q_check, self.namespaces):
                print(item.text)
            raise ValueError('Could not find %s' % journey)
        return Activity(act)
