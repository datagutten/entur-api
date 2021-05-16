from entur_api import EnturGraphQL


class EnturVehicles(EnturGraphQL):
    endpoint = 'https://api.entur.io/realtime/v1/vehicles/graphql'
    endpoint_folder = 'vehicles'

    def __init__(self, client):
        super().__init__(client)

    def vehicles(self, line, codespace='RUT') -> dict:
        """
        Get vehicles from line id
        :param line:
        :param codespace:
        :return: Dict indexed by service journey private code
        """
        query = self.get_query('vehicles')
        result = self.run_query(query, {'codespace': codespace, 'line': line})
        data = {}
        for vehicle in result['data']['vehicles']:
            public_code = \
                vehicle['serviceJourney']['serviceJourneyId'].split(':')[1]
            data[public_code] = vehicle
        return data
