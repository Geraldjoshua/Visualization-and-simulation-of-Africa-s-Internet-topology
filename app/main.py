from flask import Flask, render_template

from app import MongoOperations as mo, CaidaMeasure as cm, IpFetcher as ipf, SpeedcheckerMeasure as sc, \
    RipeMeasure as rm
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

ip_Africa_address = []
trace_done = False  # for the first initial start of trace


def timed_job_3hours():
    if len(ip_Africa_address) > 0:
        global trace_done
        trace_done = True

        sc.post_trace_all_ip_test(ip_Africa_address)
        rm.post_trace_all_ip_test(ip_Africa_address)
        cm.post_trace_all_ip_test(ip_Africa_address)


scheduler.add_job(id="postmeasurements", func=timed_job_3hours, trigger='interval', minutes=180)


def timed_job_3hours40():
    if trace_done:
        sc.get_trace_all_result()
        rm.get_trace_all_result()
        cm.get_trace_all_result()
        mo.delete_empty_traces("SpeedChecker")
        mo.delete_empty_traces("CAIDA")
        mo.delete_empty_traces("RIPE")
        mo.get_linked_asn("SpeedChecker")
        mo.get_linked_asn("CAIDA")
        mo.get_linked_asn("RIPE")
        mo.get_asn_location("SpeedChecker")
        mo.get_asn_location("CAIDA")
        mo.get_asn_location("RIPE")


scheduler.add_job(id="getmeasurements", func=timed_job_3hours40, trigger='interval', minutes=220)


def timed_job_24hours():
    global ip_Africa_address
    ipf.scrape_africa_asn()
    ip_Africa_address = ipf.get_random_africa_ip()


scheduler.add_job(id="ipaddresses", func=timed_job_24hours, trigger='interval', minutes=1440)


@app.route('/')
def index():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("SpeedChecker")
    # data = [[{"key":2,"p":5}],[{"tes":4,"les":5}]]
    return render_template("/index.html", error=False, data=data)


@app.route('/speed')
def speed():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("SpeedChecker")
    return render_template("/index.html", error=False, data=data)


@app.route('/caida')
def caida():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("CAIDA")

    return render_template("/caida.html", error=False, data=data)


@app.route('/ripe')
def ripe():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("RIPE")
    return render_template("/Ripe.html", error=False, data=data)


@app.route("/simulate")
def simulate():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("SpeedChecker")
    return render_template("/simulate.html", error=False, data=data)


@app.route("/Caidasimulate")
def caidasimulate():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("CAIDA")
    return render_template("/caidasimulate.html", error=False, data=data)


@app.route("/Ripesimulate")
def ripesimulate():
    # data array contains 2 arrays [linksarray object, nodesarray object]
    data = mo.get_topology_data("RIPE")
    return render_template("/ripesimulate.html", error=False, data=data)
