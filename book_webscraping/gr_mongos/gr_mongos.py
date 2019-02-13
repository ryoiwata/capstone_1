from pymongo import MongoClient


# Create instance of the MongoClient class
client = MongoClient()
database = client['capstone_1_db']   # Database name (to connect to)
collections = database['good_reads_collections'] # Collection name (to use)



collections.insert_one({"name" : "Sam", "friends" : [ "Scott", "Chris"], "fav_color" : "Green" })
