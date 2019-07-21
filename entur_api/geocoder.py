from .enturcommon import EnturCommon


class GeoCoder(EnturCommon):
    def reverse(self, lat, lon):
        url = 'https://api.entur.io/geocoder/v1/reverse?' \
              'point.lat=%s&point.lon=%s&lang=en&size=10&layers=venue' \
              % (lat, lon)
        result = self.get(url)
        return result['features']
