from selenium import webdriver
import selenium
import time
from lxml import html
import requests


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import requests
import re
from bs4 import BeautifulSoup
from contextlib import closing
import json
import time

session_requests = requests.session()

login_url = "https://www.goodreads.com/user/sign_in"
result = session_requests.get(login_url)

tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]

payload = {
	"user[email]": "ryoi360@gmail.com",
	"user[password]": "",
	"authenticity_token": authenticity_token
}

result = session_requests.post(login_url, data = payload, headers = dict(referer=login_url))

num = 3
url = 'https://www.goodreads.com/shelf/show/currently-reading?page={}'.format(num)

# url = "https://www.goodreads.com/user/show/75954048-ryo"
result = session_requests.get(url, headers = dict(referer = url))
# print(result.text)

soup = BeautifulSoup(result.text, 'html.parser')

for obj in soup.find_all('div',class_='left')[:5]:
	book_obj = obj.find('a',class_='bookTitle')
	book_title = obj.find('a',class_='bookTitle').text
	data_title = str(book_title).split("(")[0].strip()
	print(data_title)


# from selenium import webdriver
# import selenium
# import time
#
# browser = webdriver.Chrome('./chromedriver')
# browser.get("https://www.goodreads.com/user/sign_in")
# login_box = browser.find_element_by_css_selector("input#")
#
# search_box = browser.find_element_by_css_selector("user_email")
# search_box.click()
# search_box.send_keys("alexa")
# search_button.click()
