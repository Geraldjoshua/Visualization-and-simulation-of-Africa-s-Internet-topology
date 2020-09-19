from flask import Flask
from pymongo import MongoClient
from pymongo import  collection

Connection= "mongodb+srv://willie:admin123@testing.ac8uu.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(Connection)
db = client.get_database('flask_mongodb_atlas')
user_collection = collection.Collection(db, 'people')
