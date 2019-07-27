from xml.etree import ElementTree

from .enturcommon import EnturCommon


class Activity:
    activity = None
    namespaces = {'siri': 'http://www.siri.org.uk/siri'}

    def __init__(self, activity):
        self.activity = activity
        if not type(activity) == ElementTree.Element:
            raise ValueError('Invalid argument type: %s, should be '
                             'xml.etree.ElementTree.Element' % type(activity))
        if not activity.tag == '{http://www.siri.org.uk/siri}VehicleActivity':
            raise ValueError('Tag should be VehicleActivity, but is %s' %
                             activity.tag)

    def find(self, query, text=True, topic=None):
        if not topic:
            topic = self.activity
        result = topic.find(query, self.namespaces)

        if result is None:
            return None
        if text:
            return result.text
        else:
            return result

    def progress(self):
        return self.find('.//siri:ProgressBetweenStops/siri:Percentage')

    def line_ref(self):
        return self.find('.//siri:LineRef')

    def direction(self):
        return self.find('.//siri:DirectionRef')

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
        return self.find('.//siri:OriginName')

    def origin_time(self):
        return self.find('.//siri:OriginAimedDepartureTime')

    def destination_ref(self):
        return self.find('.//siri:DestinationRef')

    def destination(self):
        return self.find('.//siri:DestinationName')

    def destination_time(self):
        return self.find('.//siri:DestinationAimedArrivalTime')

    def monitored(self):
        text = self.find('.//siri:Monitored')
        if text == 'true':
            return True
        elif text == 'false':
            return False
        else:
            return None

    def location(self):
        location = self.find('.//siri:VehicleLocation', text=False)
        lat = self.find('siri:Latitude', topic=location)
        lon = self.find('siri:Longitude', topic=location)
        return [lat, lon]

    def location_link(self):
        [lat, lon] = self.location()
        return 'http://www.google.com/maps/place/%s,%s' % (lat, lon)

    def delay(self):
        return self.find('.//siri:Delay')

    def block_ref(self):
        return self.find('.//siri:BlockRef')

    def block_ref_num(self):
        from re import sub
        return sub(r'[A-Za-z:]+:([0-9]+):.+', r'\1', self.block_ref())

    def vehicle(self):
        return self.find('.//siri:VehicleRef')

    def visit(self, call):
        info = {'StopPointRef': self.find('siri:StopPointRef', topic=call),
                'VisitNumber': self.find('siri:VisitNumber', topic=call),
                'StopPointName': self.find('siri:StopPointName', topic=call),
                'DestinationDisplay': self.find('siri:DestinationDisplay',
                                                topic=call),
                'VehicleAtStop': self.find('siri:VehicleAtStop', topic=call),
                }
        return info

    def previous_call(self):
        call = self.find('.//siri:PreviousCalls/siri:PreviousCall', text=False)
        return self.visit(call)

    def monitored_call(self):
        call = self.find('.//siri:MonitoredCall', text=False)
        return self.visit(call)

    def onward_call(self):
        call = self.find('.//siri:OnwardCalls/siri:OnwardCall', text=False)
        return self.visit(call)

    def stop(self, category):
        if category == 'previous':
            call = self.find('.//siri:PreviousCalls/siri:PreviousCall',
                             text=False)
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
            f.close()
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

    def find_vehicle_activity(self, origin_aimed_departure_time=None,
                              origin_quay=None, line=None, debug=False):
        q = './/siri:VehicleMonitoringDelivery'
        act = self.tree.find(q, self.namespaces)
        if debug:
            print(origin_aimed_departure_time)
        if origin_aimed_departure_time:
            act = act.find('.//siri:OriginAimedDepartureTime[.="%s"]/../..' %
                           origin_aimed_departure_time, self.namespaces)
            if debug:
                print('origin_aimed_departure_time', origin_aimed_departure_time, act)
        if origin_quay:
            act = act.find('.//siri:OriginRef[.="%s"]/../..' % origin_quay,
                           self.namespaces)
            if debug:
                print('origin_quay', origin_quay, act)
        if line:
            act = act.find('.//siri:LineRef[.="%s"]/../..' % line,
                           self.namespaces)
            if debug:
                print('line', line, act)

        if act is not None:
            return Activity(act)

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
