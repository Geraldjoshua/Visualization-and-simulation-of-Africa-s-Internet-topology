import time
import pandas as pd
import SpeedcheckerMeasure as sc
import CaidaMeasure as cm
import RipeMeasure as rm
from flask import jsonify, make_response

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("/index.html", error=False)


@app.route("/simulate")
def simulate():
    return render_template("/simulate.html", error=False)


@app.route("/create-measurement", methods=["POST"])
def create_measurement():
    req = request.get_json()
    platform = str(req['platforms']).strip()
    if platform == "SpeedChecker":
        sc.get_available_probes()
        time.sleep(60)
        sc.post_trace_all_ip_test()
    elif platform == "RIPE":
        rm.post_trace_all_ip_test()
    elif platform == "CAIDA":
        cm.post_trace_all_ip_test()

    res = make_response(jsonify({"message": "OK"}), 200)

    return res


@app.route("/fetch-measurement", methods=["POST"])
def fetch_measurement():
    req = request.get_json()
    platform = str(req['platforms']).strip()
    if platform == "SpeedChecker":
        sc.get_trace_all_result()
    elif platform == "RIPE":
        rm.get_trace_all_result()
    elif platform == "CAIDA":
        cm.get_trace_all_result()

    res = make_response(jsonify({"message": "OK"}), 200)

    return res
