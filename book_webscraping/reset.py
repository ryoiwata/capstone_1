import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
# Create instance of the MongoClient class
client = MongoClient()
database = client['capstone_1_db']   # Database name (to connect to)
collections = database['good_reads_best_books'] # Collection name (to use)

try:
    collections.delete_many({})
except:
    pass
collections = database['good_reads_best_books']
