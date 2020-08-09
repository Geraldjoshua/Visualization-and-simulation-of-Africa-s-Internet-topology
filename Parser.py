import json
import MongoOperations as mo
import os

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
        with open("trace/" + a) as json_file:
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
    asn = mo.get_asn()
    if os.path.exists("files/uniqueAsn.txt"):
        os.remove("files/uniqueAsn.txt")
    f = open("files/uniqueAsn.txt", "a")
    for a in asn:
        f.write(a.strip())
        f.write("\n")
    f.close()
