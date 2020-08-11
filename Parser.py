import json

import requests

import MongoOperations as mo
import os
import subprocess

"""
    A parser script that gets ip addresses and ASN's and puts them in a txt file for processing
"""

"""
    gets ip addresses
"""


def obtain_ip_addresses():
    directory = "files/trace"
    f = open("files/ips.txt", "w", newline='')
    for filename in os.listdir(directory):
        a = filename
        with open("files/trace/" + a) as json_file:
            data = json.load(json_file)
            # print("ResponseStatus:", data['ResponseStatus'])
            # print("")
            for probeResult in data['TracerouteTestResults']:
                # print("ProbeInfo:", probeResult['ProbeInfo']['ASN'])
                # print("Destination IP:", probeResult['IP'])
                f.write(probeResult['IP'].strip())
                f.write('\n')
                for tracert in probeResult['Tracert']:
                    if tracert['IP']:
                        # print("IP:", tracert['IP'])
                        f.write(tracert['IP'].strip())
                        f.write('\n')
                # print("")


def obtain_all_asn():
    asn = mo.get_asn("SpeedChecker")
    if os.path.exists("files/uniqueAsn.txt"):
        os.remove("files/uniqueAsn.txt")
    f = open("files/uniqueAsn.txt", "a")
    for a in asn:
        f.write(str(a).strip())
        f.write("\n")
    f.close()


def get_aliases():
    #params = {'key': "ef6c77cf438ca8353f5a266498f4785b"}
    #params['task_name'] = "upload"
    #g_base_url = "https://vela.caida.org/midar-api"
    #g_timeout = 120
    #r = requests.post(g_base_url + "/upload", files="files/ips.txt", params=params,timeout=g_timeout)
    #result = r.json()
    #print(result)
    subprocess.call("python midar-api --key ef6c77cf438ca8353f5a266498f4785b upload files/ips.txt >midarid.txt", shell=True)

def get_status():
    subprocess.call("python midar-api --key ef6c77cf438ca8353f5a266498f4785b status 85",shell=True)

def get_result():
    subprocess.call("python midar-api --key ef6c77cf438ca8353f5a266498f4785b --out files/midar.sets get 85",shell=True)



def main():
    #obtain_ip_addresses()
    #obtain_all_asn()
    #get_aliases()
    #get_status()
    get_result()



if __name__ == "__main__":
    main()
