import os
from abc import ABC

import requests

from entur_api import EnturCommon


class EnturGraphQL(EnturCommon, ABC):
    endpoint: str = None
    endpoint_folder: str = None

    def __init__(self, client):
        super().__init__(client)
        self.query_folder = os.path.join(os.path.dirname(__file__),
                                         'queries',
                                         self.endpoint_folder
                                         )

    def get_query(self, query):
        file = os.path.join(self.query_folder, '%s.graphql' % query)
        with open(file) as fp:
            query = fp.read()
        return query

    # https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad
    # A simple function to use requests.post to make the API call.
    # Note the json= section.
    def run_query(self, query, variables=None):
        if variables is None:
            variables = {}
        headers = {'ET-Client-Name': self.client}
        request = requests.post(
            self.endpoint,
            json={'query': query, 'variables': variables},
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
