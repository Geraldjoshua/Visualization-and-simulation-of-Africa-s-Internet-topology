from datetime import timedelta
from flask import Flask, render_template, request
from flask import jsonify, make_response
from timeloop import Timeloop

import CaidaMeasure as cm
import IpFetcher as ipf
import MongoOperations as mo
import RipeMeasure as rm
import SpeedcheckerMeasure as sc

app = Flask(__name__)
ip_Africa_address = []
tl = Timeloop()
trace_done = False  # for the first initial start of trace


@tl.job(interval=timedelta(seconds=10800))  # 3hours  do trace route every after 3 hours
def sample_job_every_3hours():
    if len(ip_Africa_address) > 0:
        global trace_done
        trace_done = True
        sc.post_trace_all_ip_test(ip_Africa_address)
        rm.post_trace_all_ip_test(ip_Africa_address)
        cm.post_trace_all_ip_test(ip_Africa_address)
        # print("2s job current time : {}".format(time.ctime()))


@tl.job(interval=timedelta(seconds=13200))  # 3hrs.40 min do a get readings from traceroute done
def sample_job_every_3hours_40_min():
    mo.drop_mongo_collection()
    if trace_done:
        sc.get_trace_all_result()
        rm.get_trace_all_result()
        cm.get_trace_all_result()
        mo.delete_empty_traces("SpeedChecker")
        mo.delete_empty_traces("CAIDA")
        mo.delete_empty_traces("RIPE")
        # print("5s job current time : {}".format(time.ctime()))


@tl.job(interval=timedelta(seconds=86400))  # get new ipaddresses every after 24 hours
def sample_job_every_24hours():
    global ip_Africa_address
    ipf.scrape_africa_asn()
    ip_Africa_address = ipf.get_random_africa_ip()
    # print("10s job current time : {}".format(time.ctime()))


tl.start(block=False)


@app.route('/')
def index():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("SpeedChecker")
    paths = mo.get_paths("SpeedChecker")
    #data = [[{"key":2,"p":5}],[{"tes":4,"les":5}]]
    return render_template("/index.html", error=False,data=data, paths=paths)

# test to insert data to the data base
@app.route("/test")
def test():
    db.db.collection.insert_one({"name": "John", "age": 121})
    return "Connected to the data base!"


@app.route('/speed')
def speed():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("SpeedChecker")
    return render_template("/index.html", error=False,data=data)


@app.route('/caida')
def caida():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("SpeedChecker")
    return render_template("/caida.html", error=False,data=data)


@app.route('/ripe')
def ripe():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("SpeedChecker")
    return render_template("/Ripe.html", error=False,data=data)


@app.route("/simulate")
def simulate():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("SpeedChecker")
    return render_template("/simulate.html", error=False,data=data)


@app.route("/get-ipAddresses", methods=["POST"])
def get_ip_addresses():
    global ip_Africa_address
    ipf.scrape_africa_asn()
    ip_Africa_address = ipf.get_random_africa_ip()
    res = make_response(jsonify({"message": "OK"}), 200)
    return res


# not in use

@app.route("/create-measurement", methods=["POST"])
def create_measurement():
    req = request.get_json()
    # if platform == "SpeedChecker":
    sc.post_trace_all_ip_test(ip_Africa_address)
    # elif platform == "RIPE":
    rm.post_trace_all_ip_test(ip_Africa_address)
    # elif platform == "CAIDA":
    cm.post_trace_all_ip_test(ip_Africa_address)

    res = make_response(jsonify({"message": "OK"}), 200)

    return res


# not in use now
@app.route("/fetch-measurement", methods=["POST"])
def fetch_measurement():
    req = request.get_json()
    # if platform == "SpeedChecker":
    # sc.get_trace_all_result()
    # elif platform == "RIPE":
    # rm.get_trace_all_result()
    # elif platform == "CAIDA":
    # cm.get_trace_all_result()

    res = make_response(jsonify({"message": "OK"}), 200)

    return res

