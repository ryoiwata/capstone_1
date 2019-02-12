import requests
import re
from bs4 import BeautifulSoup

import json

import time

webpage = requests.get('https://www.goodreads.com/shelf/show/currently-reading')
