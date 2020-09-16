from pymongo import MongoClient
import geoip2.database
import random
import math
from geopy.geocoders import Nominatim
import numpy as np

geolocator = Nominatim(user_agent="city_geoloc")
globalUniqueNodes = []
connection = ''

def upload_to_mongo(platform, data):
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
                # do stuff
                print("hey")
            elif platform == "RIPE":

                # do stuff
                print("hey")

    connect.close()


def delete_empty_traces(platform):
    # establishing connection
    try:
        connect = MongoClient(connection)
        # print("Connected successfully!!!")
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
        print("not yet")
    elif platform == "RIPE":
        pass
        # delete all hops with result[0]=={'x': '*'}
        # result = ripe_collection.delete_many(delete_query)


def geolocate(city=None, country=None):
    '''
    Inputs city and country, or just country. Returns the lat/long coordinates of
    either the city if possible, if not, then returns lat/long of the center of the country.
    '''

    # If the city exists,
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
            # Geolocate the center of the country
            loc = geolocator.geocode(city)
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
        # print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
    db = connect.tracerouteDB

    if platform == "SpeedChecker":
        collection = db.Speedcheckerasnlocation
        for item in globalUniqueNodes:
            node_name = item[0]
            node_city = item[1]
            city_lat, city_long = geolocate(city=node_city)
            node_lat, node_long = generate_random_loc(city_lat, city_long, 1, 0.5)
            my_dict = {"ASN": str(node_name).rstrip('\r\n'), "Longitude": node_long, "Latitude": node_lat,
                       "City": str(node_city).rstrip('\r\n')}
            collection.insert_one(my_dict)
    elif platform == "CAIDA":
        # havent thought about it yet
        print("not yet")

    elif platform == "RIPE":
        # think about it later
        print("not yet")


def get_linked_asn(platform):
    # establing connection
    try:
        connect = MongoClient(connection)
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
        for x in mycol.find():
            if len(x['Tracert']) != 0:
                source = [x['Tracert'][0]['ASN'], x['Tracert'][0]['City']]
            else:
                continue

            # iterate through every element in the document's Tracert array checking set number
            for a in x['Tracert']:
                # first check if source does not have empty ASN or City
                if source[0] == '' or source[1] == '' or source[1] is None:
                    source = [a['ASN'], a['City']]
                    continue

                # first check if ASN='' or City=''
                if a['ASN'] == '' or a['City'] == '' or a['City'] is None:
                    continue

                # destination is a list variable
                destination = [a['ASN'], a['City']]
                # keep updating the destination variable until the ASN is different from source
                if source == destination:
                    continue

                sources.append(source)
                targets.append(destination)

                # to ensure first source node of iteration is not left out
                if source not in uniqueNodes:
                    uniqueNodes.append(source)

                # exchange the variables
                source = destination
                # to ensure end destination nodes are not left out
                if source not in uniqueNodes:
                    uniqueNodes.append(source)
        global globalUniqueNodes
        globalUniqueNodes = uniqueNodes
        for i in range(len(sources)):
            my_dict = {"Source_ASN": sources[i][0], "Source_City": sources[i][1], "Target_ASN": targets[i][0],
                       "Target_City": targets[i][1]}
            collection.insert_one(my_dict)

    elif platform == "CAIDA":
        # havent thought about it yet
        print("not yet")

    elif platform == "RIPE":
        # think about it later
        print("not yet")

    # df = pd.DataFrame({'Source': sources, 'Target': targets})
    # df.to_csv('files/asn_source_destination.csv', index=False, encoding='utf-8')
    # print("done and stored asn_source_destination in csv file")
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

# def main():
#     # upload_to_mongo("SpeedChecker")
#     # update_mongo_with_asn("SpeedChecker")
#     # update_mongo_with_alias_set("SpeedChecker")
#     # get_asn_location("SpeedChecker")
#     drop_mongo_collection()
#
#
# if __name__ == "__main__":
#     main()
