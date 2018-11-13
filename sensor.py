 # Copyright 2016 Hewlett Packard Enterprise Development LP
 #
 # Licensed under the Apache License, Version 2.0 (the "License"); you may
 # not use this file except in compliance with the License. You may obtain
 # a copy of the License at
 #
 #      http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 # License for the specific language governing permissions and limitations
 # under the License.

# from _redfishobject import RedfishObject
# from redfish.rest.v1 import ServerDownOrUnreachableError
import requests
import json
import sys
import re
import time
import os
import warnings


from elasticsearch import Elasticsearch
from datetime import datetime



try:
    ilo_ip = '15.212.144.95'
    ilo_username = "administrator"
    ilo_password = "12iso*help"

#     elastic_ip = os.environ['ELASTIC_IP']
#     elastic_username = os.environ['ELASTIC_USERNAME']
#     elastic_password = os.environ['ELASTIC_PASSWORD']

#     es = Elasticsearch([elastic_ip],
#                        http_auth=(elastic_username, elastic_password),
#                        scheme="http",
#                        port=9200,
#                        )
except Exception as e:
    print("- FAIL: You must pass in script name along with ilo IP / ilo username / ilo password")
    sys.exit(0)



def getSystemName():
    response = requests.get('https://%s/redfish/v1/systems/1/bios/' % ilo_ip, verify=True,
                            auth=(ilo_username, ilo_password))
    data = response.json()
    system_name = data[u'Attributes']['ServerName']
    print system_name
    return (system_name)


# Function to get lifecycle logs (LC)
def getJSONResponse(next_url):
    response = requests.get('https://%s%s' % (ilo_ip, next_url), verify=False, auth=(ilo_username, ilo_password))
    data = response.json()

    return data



def get_thermal_info():
    system_name = getSystemName()

    print(system_name)
    temp_dict = {}
    data = getJSONResponse('/redfish/v1/Chassis/System.Embedded.1/Thermal')
    id_ts = time.time()
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    for i in data[u'Temperatures']:
        temp_dict = {}
        id_ts = time.time()
        temp_dict[u'ilo_ip'] = ilo_ip,
        temp_dict[u'Server_Model'] = system_name,
        temp_dict[u'Created'] = ts
        temp_dict[u'MemberId'] = i[u'MemberId']
        temp_dict[u'MinReadingRangeTemp'] = i[u'MinReadingRangeTemp']
        temp_dict[u'Name'] = i[u'Name']
        temp_dict[u'PhysicalContext'] = i[u'PhysicalContext']
        temp_dict[u'ReadingCelsius'] = i[u'ReadingCelsius']
        temp_dict[u'Health'] = i[u'Status']['Health']
        temp_dict[u'State'] = i[u'Status']['State']
        temp_dict[u'UpperThresholdCritical'] = i[u'UpperThresholdCritical']
        temp_dict[u'UpperThresholdFatal'] = i[u'UpperThresholdFatal']

        es.create(index='temp_index', doc_type='temp_doc_' + str(ilo_ip), id=int(id_ts), body=temp_dict)
        time.sleep(3)


    return temp_dict


def get_fans_info():

    system_name = getSystemName()

    print(system_name)
    fan_dict = {}
    data = getJSONResponse('/redfish/v1/Chassis/System.Embedded.1/Thermal')

    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    for i in data[u'Fans']:
        fan_dict = {}

        id_ts = time.time()
        fan_dict[u'ilo_ip'] = ilo_ip,
        fan_dict[u'Server_Model'] = system_name,
        fan_dict[u'Created'] = ts
        fan_dict[u'FanName'] = i[u'FanName']
        fan_dict[u'LowerThresholdCritical'] = i[u'LowerThresholdCritical']
        fan_dict[u'LowerThresholdFatal'] = i[u'LowerThresholdFatal']
        fan_dict[u'LowerThresholdNonCritical'] = i[u'LowerThresholdNonCritical']
        fan_dict[u'MaxReadingRange'] = i[u'MaxReadingRange']
        fan_dict[u'MinReadingRange'] = i[u'MinReadingRange']
        fan_dict[u'Name'] = i[u'Name']
        fan_dict[u'PhysicalContext'] = i[u'PhysicalContext']
        fan_dict[u'Reading'] = i[u'Reading']
        fan_dict[u'ReadingUnits'] = i[u'ReadingUnits']
        fan_dict[u'Health'] = i[u'Status']['Health']
        fan_dict[u'State'] = i[u'Status']['State']
        fan_dict[u'MemberId'] = i[u'MemberId']

        es.create(index='fans_index', doc_type='fans_doc_' + str(ilo_ip), id=int(id_ts), body=fan_dict)
        time.sleep(3)

    return fan_dict



# while(True):
# 
#     get_thermal_info()
#     time.sleep(5)
#     get_fans_info()
#     time.sleep(5)

# if __name__ == "__main__":
#     'ILO_IP' = "15.212.144.95"
#     'ILO_USERNAME' = "administrator"
#     'ILO_PASSWORD' = "12iso*help"

   
getSystemName()