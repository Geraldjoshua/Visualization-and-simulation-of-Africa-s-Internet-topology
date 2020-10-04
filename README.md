# Visaulization-and-simulation-of-Africa-s-Internet-topology

**_We are using three internet measurement platforms to conduct internet measurements in Africa to obtain internet topology and visualize it on a map._**



⋅⋅* still in development stages but can be found here: https://africa-s-internet-topology.herokuapp.com/

⋅⋅* to **run**: outside the app folder from command line: **python wsgi.py**

⋅⋅* make sure you install all requirements: run **pip instal -r requirements.txt**

⋅⋅* note: we are using a free trial version of heroku and most times the app will be in maintenance mode since we exceed our daily memory limits everytime.

⋅⋅* Make sure you have the files GeoLite2-City.mmdb and GeoLite2-ASN.mmdb downloaded and stored in files folder to find geolocation of ASNs.
  
⋅⋅* make sure you have **api keys** for google maps, caida ark, speedchecker and RIPE Atlas.

⋅⋅* if you do not have an online MongoDB use a local MongoDB, if you have one make sure you estabish connection with it in MongoOperations.py