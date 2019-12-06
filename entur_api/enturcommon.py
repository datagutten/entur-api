from time import time

import requests


class EnturCommon:
    cache = {}
    last_request = {}

    def __init__(self, client):
        self.client = client

    def get(self, url, json=True):
        headers = {'ET-Client-Name': self.client}
        request = requests.get(url, headers=headers)
        if request.status_code == 200:
            if json:
                return request.json()
            else:
                return request.text
        else:
            raise Exception('Query failed to run by returning code of %s with URL %s' %
                            (request.status_code, url))

    def cached_get(self, url, json=True):
        if url in self.cache and time()-self.last_request[url] < 30:
            return self.cache[url]
        else:
            response = self.get(url, json)
            self.cache[url] = response
            self.last_request[url] = time()
            return response

    def rest_query(self, data_type='vm', operator='RUT', line_ref=None):
        url = 'https://api.entur.io/realtime/v1/rest/%s?' % data_type
        if operator:
            url += 'datasetId=%s&' % operator
        if line_ref:
            url += 'LineRef=%s&' % line_ref
        return self.cached_get(url, json=False)
