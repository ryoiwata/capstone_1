from selenium import webdriver
import selenium
import time
from lxml import html
import requests


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

login_url = "https://www.goodreads.com/user/sign_in"


session_requests = requests.session()
result = session_requests.get(login_url)
tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='authenticity_token']/@value")))[0]


payload = {
	"user[email]": "ryoi360@gmail.com",
	"password": "",
	"authenticity_token": authenticity_token
}

result = session_requests.post(login_url, data = payload, headers = dict(referer=login_url))

url = "https://www.goodreads.com/user/show/75954048-ryo"
result = session_requests.get(url,	headers = dict(referer = url))


tree = html.fromstring(result.content)
bucket_names = tree.xpath("//div[@class='infoBoxRowItem']/a/text()")

print(bucket_names)



"""
option = webdriver.ChromeOptions()
option.add_argument(" — incognito")
browser = webdriver.Chrome('./chromedriver')
browser.get("https://www.goodreads.com/user/sign_in")
"""



# browser.get("https://www.goodreads.com/shelf/show/currently-reading?page=1")
"""
timeout = 20
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, “//img[@class=’avatar width-full rounded-2']”)))
except TimeoutException:
    print(“Timed out waiting for page to load”)
    browser.quit()

search_box = browser.find_element_by_css_selector("input#twotabsearchtextbox")
"""
