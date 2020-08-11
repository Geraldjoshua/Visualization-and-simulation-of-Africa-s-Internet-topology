from datetime import datetime
from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    AtlasSource,
    AtlasCreateRequest
)
import random
import json

ATLAS_API_KEY = ""


def post_trace_all_ip_test():
    file = open("files/ip_Africa_address.txt", 'r')
    ip_address = file.readlines()
    ip_address = random.sample(ip_address, len(ip_address))
    file.close()
    file = open("files/country_list.txt", "r")
    african_countries = file.readlines()
    ip_start = 0
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
            start_time=datetime.utcnow(),
            key=ATLAS_API_KEY,
            measurements=measurement,
            sources=[source],
            is_oneoff=True
        )
        response = atlas_request.create()
        res = json.loads(response.text)
        print(res)
    # get multiple targets
