from xml.etree import ElementTree

from .enturcommon import EnturCommon


class Activity:
    activity = None
    namespaces = {'siri': 'http://www.siri.org.uk/siri'}

    def __init__(self, activity):
        self.activity = activity

    def find(self, query, text=True):
        result = self.activity.find(query, self.namespaces)
        if text:
            return result.text
        else:
            return result

    def line_ref(self):
        return self.find('.//siri:LineRef')

    def service_journey(self):
        return self.find('.//siri:DatedVehicleJourneyRef')

    def journey_pattern(self):
        return self.find('.//siri:JourneyPatternRef')

    def line_name(self):
        return self.find('.//siri:PublishedLineName')

    def operator(self):
        return self.find('.//siri:OperatorRef')

    def origin_ref(self):
        return self.find('.//siri:OriginRef')

    def origin(self):
        return self.find('.//siri:Origin')

    def destination_ref(self):
        return self.find('.//siri:DestinationRef')

    def destination(self):
        return self.find('.//siri:DestinationName')

    def location(self):
        location = self.find('.//siri:VehicleLocation', text=False)
        lat = location.find('siri:Latitude', self.namespaces)
        lon = location.find('siri:Longitude', self.namespaces)
        return [lat, lon]

    def delay(self):
        return self.find('.//siri:Delay')

    def block_ref(self):
        return self.find('.//siri:BlockRef')

    def block_ref_num(self):
        from re import sub
        return sub(r'[A-Za-z:]+:([0-9]+):.+', r'\1', self.block_ref())

    def vehicle(self):
        return self.find('.//siri:VehicleRef')

    def stop(self, category):
        if category == 'previous':
            call = self.find('.//siri:PreviousCalls/siri:PreviousCall', text=False)
        elif category == 'nearest':
            call = self.find('.//siri:MonitoredCall', text=False)
        elif category == 'next':
            call = self.find('.//siri:OnwardCalls/OnwardCall', text=False)
        else:
            raise ValueError('Invalid category')
        return call


class Siri(EnturCommon):

    namespaces = {'siri': 'http://www.siri.org.uk/siri'}
    tree = None

    def __init__(self, client, line=None, file=None):
        super().__init__(client)

        # print(line)
        if line:
            xml_string = self.rest_query(line_ref=line)
        elif file:
            f = open(file, 'r')
            xml_string = f.read()
        else:
            raise Exception('file or line must be specified')

        self.tree = ElementTree.fromstring(xml_string)

    def vehicle_activities(self):
        activities_xml = self.tree.findall(
            './/siri:VehicleMonitoringDelivery/siri:VehicleActivity', self.namespaces)
        activities = []
        for activity_xml in activities_xml:
            activities.append(Activity(activity_xml))

        return activities

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
        print(q)
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
