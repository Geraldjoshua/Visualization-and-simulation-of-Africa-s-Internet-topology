import time

from pymongo import MongoClient
import geoip2.database
import random
import math
from geopy.geocoders import Nominatim
import numpy as np
import os
import json

geolocator = Nominatim(user_agent="city_geoloc")
SpeedChGlobalUniqueNodes = []
CaidaGlobalUniqueNodes = []
RipeGlobalUniqueNodes = []
connection = "mongodb+srv://willie:admin123@testing.ac8uu.mongodb.net/test?retryWrites=true&w=majority"


def upload_to_mongo(platform, data):
    # establishing connection
    try:
        connect = MongoClient(connection)
        #connect = MongoClient('mongodb://localhost:27017/')

    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the database
    db = connect.tracerouteDB

    # creating or switching to Collection
    # collection = db.Speedcheckertraces

    # directory = r'C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/code/trace'
    # This creates a Reader object. You should use the same object
    # # across multiple requests as creation of it is expensive.
    # pathToDb = "files/GeoLite2-ASN.mmdb"
    # path_to_db = "files/GeoLite2-City.mmdb"
    
    with geoip2.database.Reader(pathToDb) as reader:
        with geoip2.database.Reader(path_to_db) as cityReader:
            if platform == "SpeedChecker":
                collection = db.Speedcheckertraces
                for testResult in data["TracerouteTestResults"]:
                    # append the City of the probe IP first
                    ip = testResult['IP']
                    try:
                        cityResponse = cityReader.city(ip)
                        city = cityResponse.city.name
                    except:
                        # print("Address not in database")
                        city = ""
                    # append the new fields to the testResult
                    testResult.update({"City": city})

                    # now iterate through each testResult['Tracert'] and update
                    for tracert in testResult['Tracert']:

                        ip = tracert['IP']
                        try:
                            response = reader.asn(ip)
                            cityResponse = cityReader.city(ip)
                            asn = response.autonomous_system_number
                            city = cityResponse.city.name
                        except:
                            # print("Address not in database")
                            asn = ""
                            city = ""
                        # append the new fields to the testResult
                        tracert.update({"ASN": asn})
                        tracert.update({"City": city})

                    # now insert the whole updated document into mongo
                    collection.insert_one(testResult)
            elif platform == "CAIDA":
                collection = db.Caidatraces
                #collection.drop()
                #add this before each sequence of traceroute hop documents to indicate the start of a set of traces.
                ip = data['src']
                try:
                    response = reader.asn(ip)
                    cityResponse = cityReader.city(ip)
                    asn = response.autonomous_system_number
                    city= cityResponse.city.name
                except:
                    #print("Address not in database")
                    asn = ""
                    city = ""
                source_address = { "source_address": ip, "ASN": asn, "City": city }
                collection.insert_one(source_address)

                #each traceroute hop is an individual document. 
                for testResult in data["hops"]:

                    #first discard any testResult that has empty traces
                    if testResult['addr']=="":
                        continue

                    ip = testResult['addr']

                    try:
                        response = reader.asn(ip)
                        cityResponse = cityReader.city(ip)
                        asn = response.autonomous_system_number
                        city= cityResponse.city.name
                    except:
                        #print("Address not in database")
                        asn = ""
                        city = ""

                    #append the new fields to the testResult
                    hop = { "addr": ip, "ASN": asn, "City": city }
                    collection.insert_one(hop)
            elif platform == "RIPE":
                collection = db.Ripetraces
                #collection.drop()
                #add this before each sequence of traceroute hop documents to indicate the start of a set of traces.
                ip = data['src_addr']
                try:
                    response = reader.asn(ip)
                    cityResponse = cityReader.city(ip)
                    asn = response.autonomous_system_number
                    city= cityResponse.city.name
                except:
                    #print("Address not in database")
                    asn = ""
                    city = ""
                source_address = { "source_address": ip, "ASN": asn, "City": city }
                collection.insert_one(source_address)

                #each traceroute hop is an individual document. 
                for testResult in data["result"]:

                    #first discard any testResult that has empty traces
                    if testResult['result'][0]=={'x': '*'}:
                        continue

                    ip = testResult['result'][0]['from']

                    try:
                        response = reader.asn(ip)
                        cityResponse = cityReader.city(ip)
                        asn = response.autonomous_system_number
                        city= cityResponse.city.name
                    except:
                        #print("Address not in database")
                        asn = ""
                        city = ""

                    #append the new fields to the testResult
                    testResult.update({"ASN": asn})
                    testResult.update({"City": city})
                    collection.insert_one(testResult)

    connect.close()


def delete_empty_traces(platform):
    # establishing connection
    try:
        connect = MongoClient(connection)
        #connect = MongoClient('mongodb://localhost:27017/')
    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the database
    db = connect.tracerouteDB

    if platform == "SpeedChecker":
        # creating or switching to demoCollection
        collection = db.Speedcheckertraces
        # delete all tracert elements with null IP
        qu = {}
        update = {"$pull": {"Tracert": {"IP": ""}}}
        result = collection.update_many(qu, update, upsert=True)
        print("Number of documents matched and modified: ", result.matched_count, result.modified_count)

    elif platform == "CAIDA":
        # implement
        pass
    elif platform == "RIPE":
        # creating or switching to demoCollection
        collection = db.Ripetraces
        #delete all hops with result[0]=={'x': '*'}
        delete_query = {"result.0.x": "*"}
        result = collection.delete_many(delete_query)


def geolocate(city=None, country=None, ip=None):
    '''
    Inputs city and country, or just country. Returns the lat/long coordinates of
    either the city if possible, if not, then returns lat/long of the center of the country.
    '''

    # If the country exists,
    if country is not None:
        # Try
        try:
            # To geolocate the city and country
            loc = geolocator.geocode(str(city + ',' + country))
            # And return latitude and longitude
            return loc.latitude, loc.longitude
            # Otherwise
        except:
            # Return missing value
            return np.nan
            # If the city doesn't exist
    else:
        # Try
        try:
            # Geolocate the center of the city
            loc = geolocator.geocode(city)
            if loc is None:
                path_to_db = "files/GeoLite2-City.mmdb"
                with geoip2.database.Reader(path_to_db) as reader:
                    response = reader.city(ip)
                    return response.location.latitude, response.location.longitude

            # And return latitude and longitude
            return loc.latitude, loc.longitude
            # Otherwise
        except:
            # Return missing value
            return np.nan


def generate_random_loc(longitude, latitude, num_points, max_radius):
    # brute force generate random angle and random radius
    for i in range(num_points):
        # random angle
        alpha = round(2 * math.pi * random.random(), 3)
        # random radius
        r = math.sqrt(random.uniform(0, max_radius))
        # calculating coordinates
        x = round(r * math.cos(alpha), 3) + longitude
        y = round(r * math.sin(alpha), 3) + latitude
        return x, y


def get_asn_location(platform):
    try:
        connect = MongoClient(connection)
        #connect = MongoClient('mongodb://localhost:27017/')
        # print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
    db = connect.tracerouteDB

    if platform == "SpeedChecker":
        collection = db.Speedcheckerasnlocation
        asn_location_helper(collection, SpeedChGlobalUniqueNodes)
        
    elif platform == "CAIDA":
        collection = db.Caidaasnlocation
        asn_location_helper(collection, CaidaGlobalUniqueNodes)

    elif platform == "RIPE":
        collection = db.Ripeasnlocation
        asn_location_helper(collection, RipeGlobalUniqueNodes)

def asn_location_helper(collection, uniqueNodes_arr):
    for item in uniqueNodes_arr:
        if item is not None:
            node_name = item[0]
            node_city = item[1]
            city_lat, city_long = geolocate(city=node_city, ip=item[2])
            node_lat, node_long = generate_random_loc(city_lat, city_long, 1, 0.5)
            my_dict = {"ASN": str(node_name).rstrip('\r\n'), "Longitude": node_long, "Latitude": node_lat,
                       "City": str(node_city).rstrip('\r\n')}
            collection.insert_one(my_dict)


def get_linked_asn(platform):
    # establing connection
    try:
        connect = MongoClient(connection)
        #connect = MongoClient('mongodb://localhost:27017/')
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    mydb = connect["tracerouteDB"]
    # mycol = mydb["traces"]

    if platform == "SpeedChecker":
        collection = mydb["Speedcheckerlinkedasn"]
        mycol = mydb["Speedcheckertraces"]
        sources = []
        targets = []
        uniqueNodes = []  # list of all unique nodes
        rtt_list = []
        for x in mycol.find():
            if len(x['Tracert']) != 0:
                source = [x['Tracert'][0]['ASN'], x['Tracert'][0]['City'], x['Tracert'][0]['IP']]
            else:
                continue

            # iterate through every element in the document's Tracert array checking set number
            for a in x['Tracert']:
                # first check if source does not have empty ASN or City
                if source[0] == '' or source[1] == '' or source[1] is None:
                    source = [a['ASN'], a['City'], a['IP']]
                    continue

                # first check if ASN='' or City=''
                if a['ASN'] == '' or a['City'] == '' or a['City'] is None:
                    continue

                # destination is a list variable
                destination = [a['ASN'], a['City'], a['IP']]
                # keep updating the destination variable until the ASN is different from source
                if source == destination:
                    continue

                # append rtt to source and destination
                total = 0
                if a['PingTimeArray'] is not None:
                    for rtt in a['PingTimeArray']:
                        if rtt is not None:
                            total += int(rtt)
                    avg_rtt = round(total / len(a['PingTimeArray']), 2)
                else:
                    avg_rtt = 0.0
                sources.append(source)
                targets.append(destination)
                rtt_list.append(avg_rtt)

                # to ensure first source node of iteration is not left out
                not_found = True
                if source not in uniqueNodes:
                    for item in uniqueNodes:
                        if str(source[0]).strip() == str(item[0]).strip() and str(source[1]).strip() == str(
                                item[1]).strip():
                            not_found = False
                            break
                    if not_found:
                        uniqueNodes.append(source)

                # exchange the variables
                source = destination
                # to ensure end destination nodes are not left out
                if source not in uniqueNodes:
                    for item in uniqueNodes:
                        if str(source[0]).strip() == str(item[0]).strip() and str(source[1]).strip() == str(
                                item[1]).strip():
                            not_found = False
                            break
                    if not_found:
                        uniqueNodes.append(source)
        global SpeedChGlobalUniqueNodes
        SpeedChGlobalUniqueNodes = uniqueNodes
        for i in range(len(sources)):
            my_dict = {"Source_ASN": sources[i][0], "Source_City": sources[i][1], "Target_ASN": targets[i][0],
                       "Target_City": targets[i][1], "RTT": rtt_list[i]}
            collection.insert_one(my_dict)

    elif platform == "CAIDA":
        collection = mydb["Caidalinkedasn"]
        #collection.drop()
        mycol = mydb["Caidatraces"]
        paths_col = mydb["CaidaPaths"]
        sources = []
        targets = []
        traces = []
        trace_path = []
        uniqueNodes = []  # list of all unique nodes
        rtt_list = []     #Caida does not have RTT though
        destination = []
        sourceValid = False
        for x in mycol.find():
            if not sourceValid:
                if 'source_address' in x:
                    sourceValid = False
                    #the first document is a source address for the next hops till the next source
                    source = [x['ASN'], x['City'], x['source_address']]
                else:
                    source = [x['ASN'], x['City'], x['addr']]

                #print(source)

                # iterate through every element in the document's Tracert array checking set number
                # first check if source does not have empty ASN or City
                if source[0] == '' or source[1] == '' or source[1] is None:
                    continue

                #if the code gets here, source is valid
                sourceValid = True

            else:
                #first check if we havent reached the end of the trace and need to move to the next
                if 'source_address' in x:
                    sourceValid = False
                    trace_path.append(source[:2])
                    #print(trace_path)
                    # if len(trace_path)>1:
                    #     path_dict = {"Path": trace_path}
                    #     paths_col.insert_one(path_dict)
                    trace_path.clear()
                    #reinitialize source
                    source = [x['ASN'], x['City'], x['source_address']]
                    continue

                # first check if ASN='' or City=''
                if x['ASN'] == '' or x['City'] == '' or x['City'] is None:
                    continue

                # at this point destination is now valid too
                destination = [x['ASN'], x['City'], x['addr']]
                #print(destination)
                # keep updating the destination variable until the ASN is different from source
                if source[:2] == destination[:2]:
                    continue

                #at this point we have distinct, valid source and destination
                sources.append(source)
                targets.append(destination)
                trace_path.append(source[:2])

                # to ensure first source node of iteration is not left out
                not_found = True
                if source not in uniqueNodes:
                    #uniqueNodes.append(source)
                    for item in uniqueNodes:
                        if str(source[0]).strip() == str(item[0]).strip() and str(source[1]).strip() == str(
                                item[1]).strip():
                            not_found = False
                            break
                    if not_found:
                        uniqueNodes.append(source)

                # exchange the variables
                source = destination
                # to ensure end destination nodes are not left out
                if source not in uniqueNodes:
                    #uniqueNodes.append(source)
                    for item in uniqueNodes:
                        if str(source[0]).strip() == str(item[0]).strip() and str(source[1]).strip() == str(
                                item[1]).strip():
                            not_found = False
                            break
                    if not_found:
                        uniqueNodes.append(source)
        global CaidaGlobalUniqueNodes
        CaidaGlobalUniqueNodes = uniqueNodes

        # f = open("CaidaUniqueNodes.txt", 'w', encoding="utf-8")
        # print("writing...")
        # for node in uniqueNodes:
        #     f.write(str(node)+'\n')
        # f.close()
        
        for i in range(len(sources)):
            my_dict = {"Source_ASN": sources[i][0], "Source_City": sources[i][1], "Target_ASN": targets[i][0],
                       "Target_City": targets[i][1], "RTT": 0.0}
            collection.insert_one(my_dict)

    elif platform == "RIPE":
        collection = mydb["Ripelinkedasn"]
        #collection.drop()
        mycol = mydb["Ripetraces"]
        paths_col = mydb["RipePaths"]
        sources = []
        targets = []
        traces = []
        trace_path = []
        uniqueNodes = []  # list of all unique nodes
        rtt_list = []
        destination = []
        sourceValid = False
        for x in mycol.find():
            if not sourceValid:
                if 'source_address' in x:
                    sourceValid = False
                    #the first document is a source address for the next hops till the next source
                    source = [x['ASN'], x['City'], x['source_address']]
                else:
                    source = [x['ASN'], x['City'], x['result'][0]['from']]

                # iterate through every element in the document's Tracert array checking set number
                # first check if source does not have empty ASN or City
                if source[0] == '' or source[1] == '' or source[1] is None:
                    continue

                #if the code gets here, source is valid
                sourceValid = True

            else:
                #first check if we havent reached the end of the trace and need to move to the next
                if 'source_address' in x:
                    sourceValid = False
                    trace_path.append(source[:2])
                    #print(trace_path)
                    # if len(trace_path)>1:
                    #     path_dict = {"Path": trace_path}
                    #     paths_col.insert_one(path_dict)
                    trace_path.clear()
                    #reinitialize source
                    source = [x['ASN'], x['City'], x['source_address']]
                    continue

                # first check if ASN='' or City=''
                if x['ASN'] == '' or x['City'] == '' or x['City'] is None:
                    continue

                # at this point destination is now valid too
                destination = [x['ASN'], x['City'], x['result'][0]['from']]
                # keep updating the destination variable until the ASN is different from source
                if source[:2] == destination[:2]:
                    continue

                #at this point we have distinct, valid source and destination
                trace_path.append(source[:2])

                # append rtt to source and destination
                total = 0
                for trace in x['result']:
                    total += float(trace['rtt'])
                avg_rtt = round(total / len(x['result']), 2)
                sources.append(source)
                targets.append(destination)
                rtt_list.append(avg_rtt)

                # to ensure first source node of iteration is not left out
                not_found = True
                if source not in uniqueNodes:
                    #uniqueNodes.append(source)
                    for item in uniqueNodes:
                        if str(source[0]).strip() == str(item[0]).strip() and str(source[1]).strip() == str(
                                item[1]).strip():
                            not_found = False
                            break
                    if not_found:
                        uniqueNodes.append(source)

                # exchange the variables
                source = destination
                # to ensure end destination nodes are not left out
                if source not in uniqueNodes:
                    #uniqueNodes.append(source)
                    for item in uniqueNodes:
                        if str(source[0]).strip() == str(item[0]).strip() and str(source[1]).strip() == str(
                                item[1]).strip():
                            not_found = False
                            break
                    if not_found:
                        uniqueNodes.append(source)
            
        global RipeGlobalUniqueNodes
        RipeGlobalUniqueNodes = uniqueNodes

        # f = open("RipeUniqueNodes.txt", 'w', encoding="utf-8")
        # print("writing...")
        # for node in uniqueNodes:
        #     f.write(str(node)+'\n')
        # f.close()
        
        for i in range(len(sources)):
            my_dict = {"Source_ASN": sources[i][0], "Source_City": sources[i][1], "Target_ASN": targets[i][0],
                       "Target_City": targets[i][1], "RTT": rtt_list[i]}
            collection.insert_one(my_dict)
    connect.close()


def drop_mongo_collection():
    # establing connection
    try:
        connect = MongoClient(connection)

        # print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    mydb = connect["tracerouteDB"]
    mycol_1 = mydb["Speedcheckertraces"]
    mycol_2 = mydb["Caidatraces"]
    mycol_3 = mydb["Ripetraces"]
    mycol_4 = mydb["Caidalinkedasn"]
    mycol_5 = mydb["Ripelinkedasn"]
    mycol_6 = mydb["Speedcheckerlinkedasn"]
    mycol_7 = mydb["Speedcheckerasnlocation"]
    mycol_8 = mydb["Ripeasnlocation"]
    mycol_9 = mydb["Caidaasnlocation"]
    mycol_1.drop()
    mycol_2.drop()
    mycol_3.drop()
    mycol_4.drop()
    mycol_5.drop()
    mycol_6.drop()
    mycol_7.drop()
    mycol_8.drop()
    mycol_9.drop()
    connect.close()


def upload_ping_to_mongo(platform, data):
    # establishing connection
    try:
        connect = MongoClient(connection)
        # print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the database
    db = connect.tracerouteDB

    # creating or switching to Collection
    # collection = db.Speedcheckertraces

    # directory = r'C:/Users/tshit/Documents/Blessed/Honours Courses/Honors Project/code/trace'
    # This creates a Reader object. You should use the same object
    # across multiple requests as creation of it is expensive.
    pathToDb = "files/GeoLite2-ASN.mmdb"
    path_to_db = "files/GeoLite2-City.mmdb"
    with geoip2.database.Reader(pathToDb) as reader:
        with geoip2.database.Reader(path_to_db) as cityReader:
            if platform == "SpeedChecker":
                collection = db.Speedcheckerping
                for testResult in data["TracerouteTestResults"]:
                    # append the City of the probe IP first
                    ip = testResult['IP']
                    try:
                        cityResponse = cityReader.city(ip)
                        city = cityResponse.city.name
                    except:
                        # print("Address not in database")
                        city = ""
                    # append the new fields to the testResult
                    testResult.update({"City": city})

                    # now iterate through each testResult['Tracert'] and update
                    for tracert in testResult['Tracert']:

                        ip = tracert['IP']
                        try:
                            response = reader.asn(ip)
                            cityResponse = cityReader.city(ip)
                            asn = response.autonomous_system_number
                            city = cityResponse.city.name
                        except:
                            # print("Address not in database")
                            asn = ""
                            city = ""
                        # append the new fields to the testResult
                        tracert.update({"ASN": asn})
                        tracert.update({"City": city})

                    # now insert the whole updated document into mongo
                    collection.insert_one(testResult)
            elif platform == "CAIDA":
                # do stuff
                print("hey")
            elif platform == "RIPE":
                # do stuff
                print("hey")

    connect.close()


def get_topology_data(platform):
    # establishing connection
    try:
        connect = MongoClient(connection)
        #connect = MongoClient('mongodb://localhost:27017/')
        # print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    # connecting or switching to the database
    db = connect.tracerouteDB
    if platform == "SpeedChecker":
        links = db.Speedcheckerlinkedasn
        nodes = db.Speedcheckerasnlocation
        city_nodes = db.SpeedcheckerCityLocations
    elif platform == "CAIDA":
        links = db.Caidalinkedasn
        nodes = db.Caidaasnlocation
        city_nodes = db.CaidaCityLocations
    elif platform == "RIPE":
        links = db.Ripelinkedasn
        nodes = db.Ripeasnlocation
        city_nodes = db.RipeCityLocations

    data = []
    linkdata = []
    nodedata = []
    citydata = []
    cursor = links.find()
    for record in cursor:
        dat = {"Source_ASN": record['Source_ASN'], "Source_City": record['Source_City'],
               "Target_ASN": record['Target_ASN'],
               "Target_City": record['Target_City'], "RTT": record['RTT']}
        linkdata.append(dat)
    data.append(linkdata)

    #fetch the nodes data
    cursor = nodes.find()
    for record in cursor:
        dat = {"ASN": record['ASN'], "Longitude": record['Longitude'], "Latitude": record['Latitude'],
               "City": record['City']}
        nodedata.append(dat)
    data.append(nodedata)

    #fetch city nodes data
    cursor = city_nodes.find()
    for record in cursor:
        dat = {"Longitude": record['Longitude'], "Latitude": record['Latitude'],
               "City": record['City']}
        citydata.append(dat)
    data.append(citydata)
    connect.close()
    return data

# def main():
#     upload_to_mongo("RIPE")
#     delete_empty_traces("RIPE")
#     get_linked_asn("RIPE")
#     data = get_topology_data("RIPE")
#     print(data)

# if __name__ == '__main__':
#     main()