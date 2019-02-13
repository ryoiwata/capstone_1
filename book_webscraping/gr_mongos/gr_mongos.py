from pymongo import MongoClient


# Create instance of the MongoClient class
client = MongoClient()
database = client['capstone_1_db']   # Database name (to connect to)
collections = database['good_reads_collections'] # Collection name (to use)
