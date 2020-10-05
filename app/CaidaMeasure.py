import json
import random

import requests

from app import MongoOperations as mo

"""
get all active probes in Africa
"""
api_key = ""
g_base_url = "https://vela.caida.org/api"
g_timeout = 120  # default timeout
ping_test_id = []
trace_test_id = []


def get_available_probes():
    params = {'key': api_key}
    try:
        r = requests.get(g_base_url + "/monitors", params=params, timeout=g_timeout)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"

    result = r.json()
    africa_probes = []
    if result["result"] != "error":
        ipv4 = result["ipv4"]
        temp = []
        for category in result["by_continent"]:
            if category == "Africa":
                temp = result["by_continent"]["Africa"]
                break
        for x in temp:
            if x in ipv4:
                africa_probes.append(x)
    return africa_probes


def post_trace_all_ip_test(ip_Africa_Address):
    global trace_test_id
    africa_probes = get_available_probes()
    params = {'key': api_key, "method": "traceroute"}
    ip_address = ip_Africa_Address
    ip_address = random.sample(ip_address, len(ip_address))
    ip_start = 0
    result_id = []
    for probe in africa_probes:
        for i in range(ip_start, len(ip_address)):
            if i == (ip_start + 10):
                ip_start = i
                break
            params["destination"] = str(ip_address[i])
            params["vp"] = probe
            try:
                r = requests.post(g_base_url + "/create", params=params, timeout=g_timeout)
            except requests.exceptions.RequestException as e:
                return "Request POST FAILED"

            result = r.json()
            if result["result"] != "error":
                result_id.append(result["result_id"])

    trace_test_id = result_id


def post_ping_all_ip_test(ip_Africa_Address):
    global ping_test_id
    africa_probes = get_available_probes()
    params = {'key': api_key, "method": "ping"}
    ip_address = ip_Africa_Address
    ip_address = random.sample(ip_address, len(ip_address))
    ip_start = 0
    result_id = []
    for probe in africa_probes:
        for i in range(ip_start, len(ip_address)):
            if i == (ip_start + 10):
                ip_start = i
                break
            params["destination"] = str(ip_address[i])
            params["vp"] = probe
            try:
                r = requests.post(g_base_url + "/create", params=params, timeout=g_timeout)
            except requests.exceptions.RequestException as e:
                return "Request POST FAILED"

            result = r.json()
            if result["result"] != "error":
                result_id.append(result["result_id"])

    ping_test_id = result_id


def get_trace_all_result():
    params = {'key': api_key}
    if len(trace_test_id) > 0:
        mo.drop_mongo_collection("CAIDA")
    for id in trace_test_id:
        if id is not None:
            params["id"] = str(id).strip()
            try:
                r = requests.get(g_base_url + "/results", params=params, timeout=g_timeout)
            except requests.exceptions.RequestException as e:
                return "Request GET RESULT FAILED"
            result = r.json()
            if result["result"] != "error" and result["status"] == "completed":
                for k in ["values"]:
                    for mon, v in result[k].items():
                        res = json.JSONDecoder().decode(v)
                        mo.upload_to_mongo("CAIDA", res)


def get_ping_all_result():
    params = {'key': api_key}
    for id in ping_test_id:
        if id is not None:
            params["id"] = str(id).strip()
            try:
                r = requests.get(g_base_url + "/results", params=params, timeout=g_timeout)
            except requests.exceptions.RequestException as e:
                return "Request GET RESULT FAILED"
            result = r.json()
            if result["result"] != "error" and result["status"] == "completed":
                for k in ["values"]:
                    for mon, v in result[k].items():
                        res = json.JSONDecoder().decode(v)
                        mo.upload_ping_to_mongo("CAIDA", res)

