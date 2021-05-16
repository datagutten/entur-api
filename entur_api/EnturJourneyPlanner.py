from datetime import datetime

from entur_api import EnturGraphQL


class EnturJourneyPlanner(EnturGraphQL):
    endpoint = 'https://api.entur.io/journey-planner/v2/graphql'
    endpoint_folder = 'journey-planner'

    def __init__(self, client):
        super().__init__(client)

    def stop_departures_file(self, stop_id, departures=10):
        query = self.get_query('stop_departures')
        result = self.run_query(query, {
            'stop_id': stop_id,
            'number': departures
        })
        return result['data']['stopPlace']

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
        return self.run_query(query)

    def stop_departures_app(self, stop_id, limit=100):
        query = '''query GetLinesFromStopPlaceProps {
        stopPlace(id:"%s") {
            estimatedCalls(
                numberOfDepartures: %d,
                omitNonBoarding: true,
            ) {
                quay {
                    id
                    name
                    description
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
    }''' % (stop_id, limit)
        return self.run_query(query)

    def stop_info(self, stop_id):
        query = '''query GetLinesFromStopPlaceProps {
                  stopPlace(id: "%s") {
                    name
                    description
                    latitude
                    longitude
                    id
                    transportMode
                    transportSubmode
                    adjacentSites
                    timezone
                    adjacentSites
                    quays(filterByInUse: true) {
                      id
                      name
                      description
                      publicCode
                      situations {
                        id
                        summary {
                          value
                          language
                        }
                        description {
                          value
                          language
                        }
                        validityPeriod {
                          startTime
                          endTime
                        }
                        reportType
                        severity
                      }
                    }
                  }
                }
                ''' % stop_id
        return self.run_query(query)
