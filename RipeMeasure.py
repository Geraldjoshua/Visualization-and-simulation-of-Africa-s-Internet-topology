from datetime import datetime
import os
from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    AtlasSource,
    AtlasCreateRequest,
    AtlasResultsRequest
)
import random
import json
import shutil

"note: use pygal to visualize data";

ATLAS_API_KEY = ""


def post_ping_all_ip_test():
    file = open("files/ip_Africa_address.txt", 'r')
    ip_address = file.readlines()
    ip_address = random.sample(ip_address, len(ip_address))
    file.close()
    file = open("files/country_list.txt", "r")
    african_countries = file.readlines()
    ip_start = 0
    result_id = []
    for country in african_countries:
        source = AtlasSource(
            type="country",
            value=str(country).strip(),
            requested=3,
            tags={"include": ["system-ipv4-works"]}
        )
        measurement = []
        for i in range(ip_start, len(ip_address)):
            if i == ip_start + 3:
                ip_start = i
                break
            if i == (len(ip_address) - 1):
                ip_start = 0
                continue
            ping = Ping(
                af=4,
                target=str(ip_address[i]).strip(),
                description="testing",
            )
            measurement.append(ping)

        atlas_request = AtlasCreateRequest(
            key=ATLAS_API_KEY,
            measurements=measurement,
            sources=[source],
            is_oneoff=True
        )
        (is_success, response) = atlas_request.create()
        if is_success:
            result_id.append(response['measurements'])

    if os.path.exists("files/ping_test_id.txt"):
        os.remove("files/ping_test_id.txt")
    file = open("files/ping_test_id.txt", "a")
    for tid in result_id:
        for a in tid:
            file.write(str(a))
            file.write('\n')
    file.close()


def post_trace_all_ip_test():
    file = open("files/ip_Africa_address.txt", 'r')
    ip_address = file.readlines()
    ip_address = random.sample(ip_address, len(ip_address))
    file.close()
    file = open("files/country_list.txt", "r")
    african_countries = file.readlines()
    ip_start = 0
    result_id = []
    for country in african_countries:
        source = AtlasSource(
            type="country",
            value=str(country).strip(),
            requested=3,
            tags={"include": ["system-ipv4-works"]}
        )
        measurement = []
        for i in range(ip_start, len(ip_address)):
            if i == ip_start + 3:
                ip_start = i
                break
            if i == (len(ip_address) - 1):
                ip_start = 0
                continue
            traceroute = Traceroute(
                af=4,
                target=str(ip_address[i]).strip(),
                description="testing",
                protocol="ICMP",
            )
            measurement.append(traceroute)

        atlas_request = AtlasCreateRequest(
            key=ATLAS_API_KEY,
            measurements=measurement,
            sources=[source],
            is_oneoff=True
        )
        (is_success, response) = atlas_request.create()
        if is_success:
            result_id.append(response['measurements'])

    # get multiple targets
    if os.path.exists("files/trace_test_id.txt"):
        os.remove("files/trace_test_id.txt")
    file = open("files/trace_test_id.txt", "a")
    for tid in result_id:
        for a in tid:
            file.write(str(a))
            file.write('\n')
    file.close()


def get_ping_all_result():
    if os.path.exists("files/ping"):
        shutil.rmtree("files/ping")
    file = open("files/ping_test_id.txt")
    os.mkdir("files/ping")
    result_id = file.readlines()
    for id in result_id:
        kwargs = {
            "msm_id": int(id),
        }
        is_success, results = AtlasResultsRequest(**kwargs).create()
        if is_success:
            for a in results:
                s = "files/ping/ping" + id.strip() + ".txt"
                with open(s, 'w') as outfile:
                    json.dump(a, outfile)


def get_trace_all_result():
    if os.path.exists("files/trace"):
        shutil.rmtree("files/trace")
    file = open("files/trace_test_id.txt")
    os.mkdir("files/trace")
    result_id = file.readlines()
    for id in result_id:
        kwargs = {
            "msm_id": int(id),
        }
        is_success, results = AtlasResultsRequest(**kwargs).create()
        if is_success:
            for a in results:
                s = "files/trace/trace" + id.strip() + ".txt"
                with open(s, 'w') as outfile:
                    json.dump(a, outfile)


# def main():
#     # post_trace_all_ip_test()
#     get_trace_all_result()
#
#
# if __name__ == "__main__":
#     main()
