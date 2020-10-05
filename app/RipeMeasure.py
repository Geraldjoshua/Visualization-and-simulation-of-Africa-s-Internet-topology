import random

from ripe.atlas.cousteau import (
    Ping,
    Traceroute,
    AtlasSource,
    AtlasCreateRequest,
    AtlasResultsRequest
)

from app import MongoOperations as mo

"note: use pygal to visualize data"

ATLAS_API_KEY = ""
ping_test_id = []
trace_test_id = []
African_countries = ["DZ", "AO", "BJ", "BW", "BF", "BI", "CM", "CV", "CF", "TD", "KM", "CG", "CD", "CI", "DJ",
                     "EG", "GQ", "ER", "ET", "GA", "GM", "GH", "GN", "GW", "KE", "LS", "LR", "LY", "MG", "MW",
                     "ML", "MR", "MU", "YT", "MA", "MZ", "NA", "NE", "NG", "RE", "RW", "SH", "ST", "SN", "SC",
                     "SL", "SO", "ZA", "SS", "SD", "SZ", "TZ", "TG", "TN", "UG", "EH", "ZM", "ZW"]


def post_ping_all_ip_test(ip_Africa_address):
    # file = open("files/ip_Africa_address.txt", 'r')
    global ping_test_id
    ip_address = ip_Africa_address  # file.readlines()
    ip_address = random.sample(ip_address, len(ip_address))
    african_countries = African_countries
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
        print(response)
        if is_success:
            result_id.append(response['measurements'])
    ping_test_id = result_id


def post_trace_all_ip_test(ip_Africa_address):
    global trace_test_id
    ip_address = ip_Africa_address  # file.readlines()
    ip_address = random.sample(ip_address, len(ip_address))
    african_countries = African_countries
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
            for pid in response['measurements']:
                result_id.append(pid)
            #result_id.append(response['measurements'])

    # for item in result_id:
    #     print(item)

    trace_test_id = result_id


def get_ping_all_result():
    for pid in ping_test_id:
        if pid is not None:
            kwargs = {
                "msm_id": int(pid),
            }
            is_success, results = AtlasResultsRequest(**kwargs).create()
            if is_success:
                for a in results:
                    mo.upload_ping_to_mongo("RIPE", a)


def get_trace_all_result():
    if len(trace_test_id) > 0:
        mo.drop_mongo_collection("RIPE")
    file = open("id.txt",'r')
    pp = file.readlines()
    for pid in pp:
        if pid is not None:
            kwargs = {
                "msm_id": str(pid).strip(),
            }
            is_success, results = AtlasResultsRequest(**kwargs).create()
            if is_success:
                for a in results:
                    mo.upload_to_mongo("RIPE", a)

