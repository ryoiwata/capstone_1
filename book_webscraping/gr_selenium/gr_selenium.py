from selenium import webdriver
import selenium
import time

browser = webdriver.Chrome('chromedriver')
browser.get("https://www.goodreads.com/shelf/show/currently-reading?page=1")
