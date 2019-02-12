import requests
import re
from bs4 import BeautifulSoup
from contextlib import closing
import json
import time

pg_num = 1
x = 40

# for x in range(10,20):

gr_webpage = requests.get('https://www.goodreads.com/shelf/show/currently-reading?page={}'.format(pg_num))
soup = BeautifulSoup(gr_webpage.text, 'html.parser')
soup.findAll('a',class_='bookTitle')

# for obj in soup.findAll('a',class_='bookTitle'):
#     print(obj.find()'a',class_='bookTitle')


# for obj in bs_obj.findAll('tr',{'class':re.compile('^(evenrow|oddrow)')}):


gr_webpage = requests.get('https://www.goodreads.com/shelf/show/currently-reading?page={}'.format(pg_num))
soup = BeautifulSoup(gr_webpage.text, 'html.parser')

book_names = soup.find_all('a',class_='bookTitle')
book_names_ind = book_names[x]
data_title = book_names_ind.text
link_book = "https://www.goodreads.com" + book_names_ind["href"]
# print(link_book)
# print(data_title)

book_read_times = soup.find_all('a',class_='smallText')
book_read_times_ind = book_read_times[x]
data_book_currently_reading = int(book_read_times_ind.text.split()[1])
# print(data_book_currently_reading)

book_year_ratings = soup.find_all('span',class_='greyText smallText')
book_year_ratings_ind = book_year_ratings[x]
book_year_ratings_list = book_year_ratings_ind.text.strip().split("\n")
str_book_ratings = book_year_ratings_list[1].strip().split()[0]
data_book_ratings = int("".join(str_book_ratings.split(",")))
# print(data_book_ratings)
data_book_year = book_year_ratings_list[2].strip().split()[1]
# print(data_book_year)



book_sub_page = requests.get(link_book)
book_sub_soup = BeautifulSoup(book_sub_page.text, 'html.parser')
data_language = book_sub_soup.find_all(itemprop="inLanguage")[0].text
# print(data_language)



author_names = soup.find_all('a',class_='authorName')
author_names_ind = author_names[x]
data_author = author_names_ind.text
# print(data_author)

link_author = author_names_ind["href"]
author_sub_page = requests.get(link_author)
# print(link_author)
author_sub_soup = BeautifulSoup(author_sub_page.text, 'html.parser')
author_birth_place = ""
for char in author_sub_soup.find("div", class_ = "dataTitle").next_siblings:
    if char.name == "div":
        break
    else:
        author_birth_place += str(char)
birth_country_stripped = author_birth_place.strip().split(",")[-1]
# print(birth_country_stripped)
birth_country_stripped_1 = birth_country_stripped.strip()
# print(birth_country_stripped_1)
data_birth_country = birth_country_stripped_1.split("\n")[0].strip()
if data_birth_country[0:3] == "The":
    data_birth_country = data_birth_country[4:].strip()
# print(data_birth_country)



print(data_title)
print(data_author)
print(data_language)
print(data_birth_country)
print(data_book_currently_reading)
print(data_book_ratings)
print(data_book_year)
# print(link_author)
# print(link_book)
