# Visaulization-and-simulation-of-Africa-s-Internet-topology

**_We are using three internet measurement platforms to conduct internet measurements in Africa to obtain internet topology that we can visualize and simulate different scenarios on a map for research and learning purpose._**



* A live web application is still in development stages but can be found here: https://africa-s-internet-topology.herokuapp.com/

* to **run** web app locally, outside the app folder from command line: run **python wsgi.py**

* a local host link of where the app is ran will appear, click to see the loacally ran web app.

* make sure you install all requirements: run **pip install -r requirements.txt**

* **_note_**: we are using a free trial version of heroku and most times the app will be in maintenance mode since we exceed our daily memory limits everytime.

* Make sure you have the files GeoLite2-City.mmdb, GeoLite2-ASN.mmdb and ipsasn.dat downloaded and stored in files folder to find geolocation of ASNs.
  
* make sure you have **api keys** for google maps, caida ark, speedchecker and RIPE Atlas.

* if you do not have an online MongoDB use a local MongoDB, if you have one make sure you estabish connection with it in MongoOperations.py
