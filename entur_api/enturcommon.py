import requests


class EnturCommon:
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
            raise Exception('Query failed to run by returning code of %s' %
                            request.status_code)

    def rest_query(self, data_type='vm', operator='RUT', line_ref=None):
        url = 'http://api.entur.org/anshar/1.0/rest/%s?' % data_type
        if operator:
            url += 'datasetId=%s&' % operator
        if line_ref:
            url += 'LineRef=%s&' % line_ref
        # print(url)
        return self.get(url, json=False)
