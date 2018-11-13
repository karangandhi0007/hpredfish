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

import sys
from _redfishobject import RedfishObject
from redfish.rest.v1 import ServerDownOrUnreachableError


        
def proc_sensors(redfishobj):
    sys.stdout.write("\nEXAMPLE 1: Report ProcMetrics \n")
    instances = redfishobj.search_for_type("Processor")
    
    for instance in instances:
        response = redfishobj.redfish_get(instance["@odata.id"])
        #print response
    new_dict = response.dict["Members"][0]
    #print new_dict
    resp = redfishobj.redfish_get(new_dict["@odata.id"])
    #print resp
    new_dict1 = resp.dict["Oem"]["Hpe"]
    #print new_dict1
    for key, value in new_dict1.items():
        if 'RatedSpeedMHz' in key:
#             print key, ":", value
            mem = {}
            mem[key] = value
#     print mem
    new_dict2 = {}
    new_dict2['ProcMetrics'] = mem
    print new_dict2
    return new_dict2
    #print new_dict1

def power_sensors(redfishobj):
    sys.stdout.write("\nEXAMPLE 2: Report PowerMetrics \n")
    instances = redfishobj.search_for_type("Power")
    
    for instance in instances:
        response = redfishobj.redfish_get(instance["@odata.id"])
        new_dict = response.dict['PowerControl'][0]['PowerMetrics']
        new_dict1 = response.dict["PowerSupplies"][0]
        for key, value in new_dict1.items():
            if 'LastPowerOutputWatts' in key:
                #print key, ":", value
                pwr = {}
                pwr[key] = value
                #print pwr
                new_dict.update(pwr)
        new_dict2 = {}
        new_dict2['PowerMetrics'] = new_dict
        print new_dict2
        return new_dict2
    return

def fan_sensors(redfishobj):
    sys.stdout.write("\nEXAMPLE 3: Report FanMetrics \n")
    instances = redfishobj.search_for_type("Thermal")
    
    for instance in instances:
        response = redfishobj.redfish_get(instance["@odata.id"])
        #print response
    new_dict = response.dict["Fans"][0]
    #print new_dict
    new_dict1 = {}
    count = 0
    for key, value in new_dict.items():
        if "Name" in key:
            #print key, ":", value
            pwr = {}
            pwr[key] = value
            new_dict1.update(pwr)
            #print pwr
        elif 'Reading' in key:
            abc = {}
            abc[key] = value
            new_dict1.update(abc)
    new_dict2 = {}
    new_dict2['FanMetrics'] = new_dict1
    print new_dict2
    return new_dict2
    
def temperature_sensors(redfishobj):
    sys.stdout.write("\nEXAMPLE 4: Report TemperatureMetrics \n")
    instances = redfishobj.search_for_type("Thermal")
    
    for instance in instances:
        response = redfishobj.redfish_get(instance["@odata.id"])
        #print response
    new_dict = response.dict["Temperatures"][0]
#     print new_dict
    new_dict1 = {}
    count = 0
    for key, value in new_dict.items():
        if "Name" in key:
            #print key, ":", value
            pwr = {}
            pwr[key] = value
            new_dict1.update(pwr)
            #print pwr
        elif 'ReadingCelsius' in key:
            abc = {}
            abc[key] = value
            new_dict1.update(abc)
    new_dict2 = {}
    new_dict2['TempMetrics'] = new_dict1
    print new_dict2
    return new_dict2          
    
if __name__ == "__main__":
    # When running on the server locally use the following commented values
    # iLO_https_url = "blobstore://."
    # iLO_account = "None"
    # iLO_password = "None"

    # When running remotely connect using the iLO secured (https://) address, 
    # iLO account name, and password to send https requests
    # iLO_https_url acceptable examples:
    # "https://10.0.0.100"
    # "https://f250asha.americas.hpqcorp.net"
    iLO_https_url = "https://15.212.144.95"
    iLO_account = "administrator"
    iLO_password = "12iso*help"

    # Create a REDFISH object
    try:
        REDFISH_OBJ = RedfishObject(iLO_https_url, iLO_account, iLO_password)
    except ServerDownOrUnreachableError as excp:
        sys.stderr.write("ERROR: server not reachable or doesn't support " \
                                                                "RedFish.\n")
        sys.exit()
    except Exception as excp:
        raise excp

    proc_sensors(REDFISH_OBJ)
    power_sensors(REDFISH_OBJ)
    fan_sensors(REDFISH_OBJ)
    temperature_sensors(REDFISH_OBJ)
    REDFISH_OBJ.redfish_client.logout()