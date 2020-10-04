"""
This is used to start the automation process when the web app is deployed on heroku
if you running it in development stage it is not going to be in use
"""

from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from app import MongoOperations as mo, CaidaMeasure as cm, IpFetcher as ipf, SpeedcheckerMeasure as sc, \
    RipeMeasure as rm

ip_Africa_address = []
trace_done = False  # for the first initial start of trace

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=180)  # 180
def timed_job_3hours():
    if len(ip_Africa_address) > 0:
        global trace_done
        trace_done = True
        sc.post_trace_all_ip_test(ip_Africa_address)
        rm.post_trace_all_ip_test(ip_Africa_address)
        cm.post_trace_all_ip_test(ip_Africa_address)


@sched.scheduled_job('interval', minutes=220)  # 220
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


@sched.scheduled_job('interval', minutes=1440)  # 1440
def timed_job_24hours():
    global ip_Africa_address
    ipf.scrape_africa_asn()
    ip_Africa_address = ipf.get_random_africa_ip()
    # print(len(ip_Africa_address))


"""
Making a get request every 25 minutes to keep the app alive and 
not to go on sleep mode since we are using the free version of heroku
"""


@sched.scheduled_job('interval', minutes=25)
def timed_job_3hours():
    response = requests.get('https://africa-s-internet-topology.herokuapp.com/')
    print(response.url)


sched.start()
