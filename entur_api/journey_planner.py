from datetime import datetime

import requests


class EnturApi:
    client = None

    def __init__(self, client):
        self.client = client

    # https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad
    # A simple function to use requests.post to make the API call.
    # Note the json= section.
    def run_query(self, query):
        headers = {'ET-Client-Name': self.client}
        request = requests.post(
            'https://api.entur.io/journey-planner/v2/graphql',
            json={'query': query},
            headers=headers)
        if request.status_code == 200:
            json = request.json()
            if 'errors' in json:
                raise Exception('Entur returned error: %s' %
                                json['errors'][0]['message'])
            return request.json()
        else:
            raise Exception('Query failed to run by returning code of {}. {}'.
                            format(request.status_code, query))

    def get(self, url, json=True):
        headers = {'ET-Client-Name': self.client}
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            if json:
                return request.json()
            else:
                return request.text
        else:
            raise Exception('Query failed to run by returning code of %s' %
                            request.status_code)

    def rest_query(self, data_type='vm', operator='RUT', line_ref=None):
        url = 'http://api.entur.org/anshar/1.0/rest/%s?' % data_type
        if operator:
            url += 'datasetId=%s&' % operator
        if line_ref:
            url += 'LineRef=%s&' % line_ref
        print(url)
        return self.get(url, json=False)

    def geocode_reverse(self, lat, lon):
        url = 'https://api.entur.org/api/geocoder/1.1/reverse?point.lat=%s&point.lon=%s&lang=en&size=10&layers=venue' \
              % (lat, lon)
        result = self.get(url)
        return result['features']

    def stop_departures(self, stop_id, start_time='',
                        departures=10, time_range=72100):
        if start_time:
            start_time = datetime.now().strftime('%Y-%m-%dT') + start_time
            start_time = \
                '(startTime:"%s" timeRange: %d, numberOfDepartures: %d)' % \
                (start_time, time_range, departures)
        query = '''{
          stopPlace(id: "%s") {
            id
            name
            estimatedCalls%s {
              aimedArrivalTime
              aimedDepartureTime
              expectedArrivalTime
              expectedDepartureTime
              realtime
              date
              forBoarding
              forAlighting
              destinationDisplay {
                frontText
              }
              quay {
                id
              }
              serviceJourney {
              id
                journeyPattern {
                  id
                  name
                  line {
                    id
                    name
                    transportMode
                  }
                }
              }
            }
          }
        }''' % (stop_id, start_time)
        # print(query)
        return self.run_query(query)

    def stop_departures_app(self, stop_id):
        query = '''query GetLinesFromStopPlaceProps {
        stopPlace(id:"%s") {
            name
            latitude
            longitude
            id
            estimatedCalls(
                numberOfDepartures: 100,
                omitNonBoarding: true,
            ) {
                quay {
                    id
                    name
                    publicCode
                }
                destinationDisplay { frontText }
                serviceJourney { id journeyPattern { line { ...lineFields } } }
                realtime
                expectedDepartureTime
                aimedDepartureTime
            }
        }
    }

    fragment lineFields on Line {
        id
        authority { id name }
        name
        publicCode
        transportMode
        transportSubmode
    }''' % stop_id
        return self.run_query(query)
