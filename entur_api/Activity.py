from xml.etree import ElementTree


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

    def __str__(self):
        return '%s %s from %s at %s' % (
        self.line_name(), self.destination(), self.origin(),
        self.origin_time())

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
