# Visualization-and-simulation-of-Africa-s-Internet-topology

**A. Preamble**

This project involved building an online visualizer and simulator for Africa's Internet Topology.

To visualize the the topology, internet measurements are taken from Speedchecker (https://www.speedchecker.com/probeapi/),
CAIDA (https://www.caida.org/home/), RIPE Atlas (https://www.ripe.net/). 

Traceroutes measurements are collected from the platforms. Remember that these internet measuring platforms uses active probing method of collecting
internet measurements. After obtaining these traceroutes, they are stored in Mongo DB online (https://www.mongodb.com/) where they later are obtained
and processed. The processing of the traceoutes involves modelling nodes and links from the traceroutes.
Links and nodes are then used to map the internet topology **(Visualization)** which is later used for **Simulation** purposes.

* A live web application is still in development stage (mostly on maintenace) but can be found here: https://africa-s-internet-topology.herokuapp.com/

**B. Code Sections:**

   1. Templates is the folder that contains the HTML code that  make ups the web pages of the platform. 
 
     1.1 caida.html contains the code for Topology Visualization with measurements collected from CAIDA.  
     
     1.2 Ripe.html contains the code for Topology Visualization with measurements collected from RIPE Atlas.
     
     1.3 index.html contains the code for Topology Visualization with measurements collected from Speedcahecker.
     
     1.4 simulate.html contains the code for Topology simulation with measurements collected from Speedchecker.
     
     1.5 caidasimulate.html contains the code for Topology simulation with measurements collected from CAIDA
     
     1.6 ripesimulate.html contains the code for Topology simulation with measurements collected from RIPE Atlas.
     
     1.7 usermanual.html contains the code for User Manual page for simulation purposes. 
     
     1.8 style.css contains the css styles for the web pages. 
  
  2. RipeMeasure.py is a python script responsible to collect measurements from RIPE python API. 
  
  3. CaidaMeasure.py is a python script responsible to collect measurements from CAIDA python API.
  
  4. SpeedCheckerMeasure.py is a python script responsible to collect measurements from SpeedChecker python API.
 
  5. MongoOperations.py is a python script where mongo operations of storing and retrieveing data has been implemented. 
  
  6. Api_test.py is a python script where the CAIDA, Speedchecker and Ripe API testing is done. The testing checks if the API is working well
  and getting the right data. 
  
  7. IpFetcher.py is a python script where African IP adresses are scrapped from the traceroutes retrieved from the DB. Scrapes African asns from ipinfo.io
  
  8. main.py is python script which describes the routing of the HTML pages. It describes how the flask server 
   should handle the web pages. It also connects the Front end and the back end of the platform by obtaining data from
   DB and parsing it to HTML pages (Front end)
  
  9. Clock.py is a python script used to start the automation process when the web app is deployed on heroku
 if you running it in development stage it is not going to be in use

 10. wsgi.py is the automation bundle for the whole web application.  
 
* A live web application is still in development stage (mostly on maintenace) but can be found here: https://africa-s-internet-topology.herokuapp.com/

* to **run** web app locally, outside the app folder from command line: run **python wsgi.py**

* a local host link of where the app is ran will appear, click to see the loacally ran web app.

* make sure you install all requirements: run **pip install -r requirements.txt**

* **_note_**: we are using a free trial version of heroku and most times the app will be in maintenance mode since we exceed our daily memory limits everytime.

* Make sure you have the files GeoLite2-City.mmdb, GeoLite2-ASN.mmdb and ipsasn.dat downloaded and stored in files folder to find geolocation of ASNs.
  
* make sure you have **api keys** for google maps, caida ark, speedchecker and RIPE Atlas.

* if you do not have an online MongoDB use a local MongoDB, if you have one make sure you estabish connection with it in MongoOperations.py

Authors 

**Willie Macharia (https://github.com/willie84)**

**Blessed Chitamba (https://github.com/blessedchitamba)**

**Gerald Ngumbulu (https://github.com/Geraldjoshua)**
