import json
import random

import requests

import MongoOperations as mo

"""
get all active probes in Africa
"""
api_key = "ef6c77cf438ca8353f5a266498f4785b"
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
    #file = open("files/ip_Africa_address.txt", 'r')
    ip_address = ip_Africa_Address #file.readlines()
    ip_address = random.sample(ip_address, len(ip_address))
    #file.close()
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
    # if os.path.exists("files/trace_test_id.txt"):
    #     os.remove("files/trace_test_id.txt")
    # file = open("files/trace_test_id.txt", "a")
    # for tid in result_id:
    #     file.write(str(tid))
    #     file.write('\n')
    # file.close()


def post_ping_all_ip_test(ip_Africa_Address):
    global ping_test_id
    africa_probes = get_available_probes()
    params = {'key': api_key, "method": "ping"}
    #file = open("files/ip_Africa_address.txt", 'r')
    ip_address = ip_Africa_Address #file.readlines()
    ip_address = random.sample(ip_address, len(ip_address))
    #file.close()
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
    # if os.path.exists("files/ping_test_id.txt"):
    #     os.remove("files/ping_test_id.txt")
    # file = open("files/ping_test_id.txt", "a")
    # for tid in result_id:
    #     file.write(str(tid))
    #     file.write('\n')
    # file.close()


def get_trace_all_result():
    # if os.path.exists("files/trace"):
    #     shutil.rmtree("files/trace")
    #
    params = {'key': api_key}
    # os.mkdir("files/trace")
    # file = open("files/trace_test_id.txt")
    # result_id = file.readlines()
    for id in trace_test_id:
        if id is not None:
            params["id"] = id.strip()
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
                        # s = "files/trace/trace" + id.strip() + ".txt"
                        # with open(s, 'w') as outfile:
                        #     json.dump(json.JSONDecoder().decode(v), outfile)


def get_ping_all_result():
    # if os.path.exists("files/ping"):
    #     shutil.rmtree("files/ping")
    params = {'key': api_key}
    # file = open("files/ping_test_id.txt")
    # os.mkdir("files/ping")
    # result_id = file.readlines()
    for id in ping_test_id:
        if id is not None:
            params["id"] = id
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
                        # s = "files/ping/ping" + id.strip() + ".txt"
                        # with open(s, 'w') as outfile:
                        #     json.dump(json.JSONDecoder().decode(v), outfile)


# def main():
#     post_trace_all_ip_test()
#     post_ping_all_ip_test()
#     time.sleep(2400)
#     get_trace_all_result()
#     get_ping_all_result()
#
#
# if __name__ == "__main__":
#     main()
