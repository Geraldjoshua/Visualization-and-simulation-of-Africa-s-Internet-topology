import shutil

import requests
import json
import os
import random

"""
get all active probes in Africa
"""


def get_available_probes():
    african_countries = []
    file = open("files/country_list.txt", "r")
    for country in file:
        country = country.split()
        african_countries.append(country[0])
    file.close()
    african_countries = random.sample(african_countries, len(african_countries))
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apikey": "7295deda-f359-4ac9-918f-93fdc01992a8"
    }
    url = "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/GetProbes?apikey=7295deda-f359-4ac9-918f-93fdc01992a8"

    # check if Africa_probes_id file exists and delete it.
    if os.path.exists("files/Africa_probes_id.txt"):
        os.remove("files/Africa_probes_id.txt")

    # check which country has probes
    for country in african_countries:
        payload = {
            "criteria": {
                "Sources": [
                    {
                        "CountryCode": str(country)
                    }
                ],
                "ProbeInfoProperties": [
                    "Latitude",
                    "Longitude",
                    "ProbeID",
                    "CountryCode",
                    "CityName",
                    "IPAddress",
                    "ASN"
                ]
            }
        }
        data = json.dumps(payload)
        try:
            r = requests.post(url, data=data, headers=headers)
        except requests.exceptions.RequestException as e:
            return "Request FAILED"
        json_result = r.json()
        file = open("files/Africa_probes_id.txt", "a")
        for probes in json_result['GetProbesResult']['Probes']:
            if probes['ProbeID'] != 'NONE':
                file.write(probes['ProbeID'])
                file.write('\n')
        file.close()


"""
doing a ping given a list of destination ip address
"""


def post_ping_all_ip_test():
    file = open("files/Africa_probes_id.txt", 'r')
    probe_id = file.readlines()
    probe_id = random.sample(probe_id, len(probe_id))
    file.close()
    file = open("files/ip_Africa_address.txt", 'r')
    ip_address = file.readlines()
    ip_address = random.sample(ip_address, len(ip_address))
    file.close()
    ip_start = 0
    url = 'https://kong.speedcheckerapi.com:8443/ProbeAPIv2/StartPingTest'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apikey": "7295deda-f359-4ac9-918f-93fdc01992a8",

    }
    test_res = []
    for probe in probe_id:
        numb_of_dest = 0
        id = probe.strip()
        for i in range(ip_start, len(ip_address)):
            ip = ip_address[i].strip()
            if numb_of_dest > 1:
                if i == (len(ip_address) - 1):
                    ip_start = 0
                else:
                    ip_start = i
                break
            if i == (len(ip_address) - 1):
                ip_start = 0
            payload = {
                "testSettings": {
                    "PingType": "icmp",
                    "Count": 3,
                    "Timeout": 4000,
                    "TestCount": 1,
                    "Sources": [
                        {
                            "ProbeID": id

                        }
                    ],
                    "Destinations": [
                        ip
                    ],
                    "ProbeInfoProperties": [
                        "ASN",
                        "CountryCode",
                    ]
                }

            }
            data = json.dumps(payload)

            try:
                r = requests.post(url, data=data, headers=headers)

            except requests.exceptions.RequestException as e:
                return "Request failed"
            res = json.loads(r.text)
            if "OK" == res['StartPingTestResult']['Status']['StatusText']:
                test_res.append(res['StartPingTestResult']['TestID'])
            else:
                print(res)
                print("failed")
            numb_of_dest += 1

    if os.path.exists("files/ping_test_id.txt"):
        os.remove("files/ping_test_id.txt")
    file = open("files/ping_test_id.txt", "a")
    for tid in test_res:
        file.write(tid)
        file.write('\n')
    file.close()


"""
returning ping results for a list of destination ip address
"""


def get_ping_all_result():
    if os.path.exists("files/ping"):
        shutil.rmtree("files/ping")
    API_ENDPOINT = "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/"
    APIKEY = "7295deda-f359-4ac9-918f-93fdc01992a8"
    os.mkdir("files/ping")
    file = open("files/ping_test_id.txt", "r")
    ping_results = file.readlines()
    for result in ping_results:
        testID = result.strip()
        url = API_ENDPOINT + "GetPingResults?apikey=" + APIKEY + "&testID=" + testID
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": "7295deda-f359-4ac9-918f-93fdc01992a8",

        }
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            print("empty")
        res = json.loads(r.text)
        if "200" == res['ResponseStatus']['StatusCode']:
            s = "files/ping/ping" + testID + ".txt"
            with open(s, 'w') as outfile:
                json.dump(res, outfile)


"""
doing a trace given a list of destination ip address
"""


def post_trace_all_ip_test():
    file = open("files/Africa_probes_id.txt", 'r')
    probe_id = file.readlines()
    probe_id = random.sample(probe_id, len(probe_id))
    file.close()
    file = open("files/ip_Africa_address.txt", 'r')
    ip_address = file.readlines()
    ip_address = random.sample(ip_address, len(ip_address))
    file.close()
    ip_start = 0
    url = 'https://kong.speedcheckerapi.com:8443/ProbeAPIv2/StartTracertTest'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apikey": "7295deda-f359-4ac9-918f-93fdc01992a8",

    }
    test_res = []
    for probe in probe_id:
        numb_of_dest = 0
        id = probe.strip()
        for i in range(ip_start, len(ip_address)):
            ip = ip_address[i].strip()
            if numb_of_dest > 1:
                if i == (len(ip_address) - 1):
                    ip_start = 0
                else:
                    ip_start = i
                break
            if i == (len(ip_address) - 1):
                ip_start = 0
            payload = {
                "testSettings": {
                    "BufferSize": 32,
                    "Count": 3,
                    "Fragment": 1,
                    "Ipv4only": 0,
                    "Ipv6only": 0,
                    "MaxFailedHops": 0,
                    "Resolve": 1,
                    "Sleep": 300,
                    "Ttl": 128,
                    "TtlStart": 1,
                    "Timeout": 80000,
                    "HopTimeout": 3000,
                    "TestCount": 1,
                    "Sources": [
                        {
                            "ProbeID": id

                        }
                    ],
                    "Destinations": [
                        ip
                    ],
                    "ProbeInfoProperties": [
                        "ASN",
                        "CountryCode",
                    ]
                }

            }
            data = json.dumps(payload)

            try:
                r = requests.post(url, data=data, headers=headers)

            except requests.exceptions.RequestException as e:
                return "Request failed"
            res = json.loads(r.text)
            if "OK" == res['StartPingTestResult']['Status']['StatusText']:
                test_res.append(res['StartPingTestResult']['TestID'])
            else:
                print(res)
                print("failed")
            numb_of_dest += 1

    if os.path.exists("files/trace_test_id.txt"):
        os.remove("files/trace_test_id.txt")
    file = open("files/trace_test_id.txt", "a")
    for tid in test_res:
        file.write(tid)
        file.write('\n')
    file.close()


"""
returning trace results for a list of destination ip address
"""


def get_trace_all_result():
    if os.path.exists("files/trace"):
        shutil.rmtree("files/trace")
    API_ENDPOINT = "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/"
    APIKEY = "7295deda-f359-4ac9-918f-93fdc01992a8"
    os.mkdir("files/trace")
    file = open("files/trace_test_id.txt", "r")
    trace_results = file.readlines()
    for result in trace_results:
        testID = result.strip()
        url = API_ENDPOINT + "GetPingResults?apikey=" + APIKEY + "&testID=" + testID
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "apikey": "7295deda-f359-4ac9-918f-93fdc01992a8",

        }
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            print("empty")
        res = json.loads(r.text)
        if "200" == res['ResponseStatus']['StatusCode']:
            s = "files/trace/trace" + testID + ".txt"
            with open(s, 'w') as outfile:
                json.dump(res, outfile)


def main():
    #get_available_probes()
    #post_ping_all_ip_test()
    get_ping_all_result()


if __name__ == "__main__":
    main()
