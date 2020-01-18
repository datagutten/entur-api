import os

from entur_api.enturcommon import EnturCommon

operator = 'RUT'
data_type = 'vm'

entur = EnturCommon('datagutten-entur-api-vm-saver')
xml_string = entur.rest_query(operator=operator, force_get=True)

file = entur.cache_file(data_type, operator)

f = open(file+'tmp', 'w')
f.write(xml_string)
f.close()

os.rename(file + 'tmp', file)

