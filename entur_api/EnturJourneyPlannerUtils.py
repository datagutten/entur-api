from entur_api import EnturJourneyPlanner


class EnturJourneyPlannerUtils(EnturJourneyPlanner):

    def filter_departures(self, stop=None, departures=None,
                          quays=None, limit=None):
        if stop is not None:
            departures = self.stop_departures_app(stop)
        elif departures is None:
            raise AttributeError('stop or departures must be specified')

        if departures['data']['stopPlace'] is None:
            raise Exception('No departures found')

        departures_filtered = []
        # print(departures)
        counter = 1
        for departure in departures['data']['stopPlace']['estimatedCalls']:
            if quays and departure['quay']['id'] not in quays:
                # print("Skip quay %s" % departure['quay'])
                continue
            departures_filtered.append(departure)
            counter += 1
            if limit and counter > limit:
                break
        return departures_filtered
