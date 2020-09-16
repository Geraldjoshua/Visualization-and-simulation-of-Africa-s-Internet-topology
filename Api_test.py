import requests
import json

from ripe.atlas.cousteau import AtlasResultsRequest

"""test endpoints in Speedchecker: get trace results
    ,get ping results,
"""


def test_get_speed_trace_result_check_status_code_equals_200():
    ApiKey = "7295deda-f359-4ac9-918f-93fdc01992a8"
    API_ENDPOINT = "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/"
    testID = ""
    url = API_ENDPOINT + "GetTracertResults?apikey=" + ApiKey + "&testID=" + testID
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apikey": ApiKey,

    }
    response = requests.get(url, headers=headers)
    res = json.loads(response.text)
    assert "200" == res['ResponseStatus']['StatusCode']


def test_get_speed_ping_result_check_status_code_equals_200():
    ApiKey = "7295deda-f359-4ac9-918f-93fdc01992a8"
    API_ENDPOINT = "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/"
    testID = ""
    url = API_ENDPOINT + "GetPingResults?apikey=" + ApiKey + "&testID=" + testID
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apikey": ApiKey,

    }
    response = requests.get(url, headers=headers)
    res = json.loads(response.text)
    assert "200" == res['ResponseStatus']['StatusCode']


"""test endpoints in RipeAtlas: get trace results
    ,get ping results,
"""


def test_get_ripe_trace_and_ping_result_check_status_is_success():
    kwargs = {
        "msm_id": 26958698,
    }
    is_success, results = AtlasResultsRequest(**kwargs).create()
    if is_success:
        assert True

    "Ping result"
    kwargs = {
        "msm_id": 26783366,
    }
    is_success, results = AtlasResultsRequest(**kwargs).create()
    if is_success:
        assert True


"""test endpoints in Caida: get trace results
    ,get ping results,
"""


def test_get_caida_trace_result_check_status_code_equals_200():
    api_key = "ef6c77cf438ca8353f5a266498f4785b"
    g_base_url = "https://vela.caida.org/api"
    g_timeout = 120  # default timeout
    id = ""
    params = {'key': api_key, "id": id.strip()}
    r = requests.get(g_base_url + "/results", params=params, timeout=g_timeout)
    assert r.status_code == 200


def test_get_caida_ping_result_check_status_code_equals_200():
    api_key = "ef6c77cf438ca8353f5a266498f4785b"
    g_base_url = "https://vela.caida.org/api"
    g_timeout = 120  # default timeout
    id = ""
    params = {'key': api_key, "id": id.strip()}
    r = requests.get(g_base_url + "/results", params=params, timeout=g_timeout)
    assert r.status_code == 200
