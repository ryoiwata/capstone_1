import pymongo
import pandas as pd
from pymongo import MongoClient
client = MongoClient()
db = client.capstone_1_db
collection = db.good_reads_collections
data = pd.DataFrame(list(collection.find()))
