import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
# Create instance of the MongoClient class
client = MongoClient()
database = client['capstone_1_db']   # Database name (to connect to)
collections = database['good_reads_collections'] # Collection name (to use)
try:
    collections.delete_many({})
except:
    pass
collections = database['good_reads_collections'] # Collection name (to use)

pg_num = 1
gr_webpage = requests.get('https://www.goodreads.com/shelf/show/currently-reading?page={}'.format(pg_num))
soup = BeautifulSoup(gr_webpage.text, 'html.parser')
for obj in soup.findAll('div',class_='left'):
    book_obj = obj.find('a',class_='bookTitle')

    book_title = obj.find('a',class_='bookTitle').text
    data_title = str(book_title).split("(")[0].strip()
    link_book = "https://www.goodreads.com" + book_obj["href"]
    # print(link_book)
    # print(data_title)
    book_read_times = obj.find('a',class_='smallText')
    data_book_currently_reading = int(book_read_times.text.split()[1])
    # print(data_book_currently_reading)

    book_year_ratings = obj.find('span',class_='greyText smallText')
    book_year_ratings_list = book_year_ratings.text.strip().split("\n")
    str_book_ratings = book_year_ratings_list[1].strip().split()[0]
    data_book_ratings = int("".join(str_book_ratings.split(",")))
    # print(data_book_ratings)
    data_book_year = int(book_year_ratings_list[2].strip().split()[1])
    # print(data_book_year)

    book_sub_page = requests.get(link_book)
    book_sub_soup = BeautifulSoup(book_sub_page.text, 'html.parser')
    try:
        data_language = book_sub_soup.find_all(itemprop="inLanguage")[0].text
    except:
        data_language = "N/A"
    # print(data_language)

    author_names = obj.find('a',class_='authorName')
    data_author = author_names.text
    # print(data_author)

    link_author = author_names["href"]
    author_sub_page = requests.get(link_author)
    # print(link_author)
    author_sub_soup = BeautifulSoup(author_sub_page.text, 'html.parser')
    author_birth_place = ""
    for char in author_sub_soup.find("div", class_ = "dataTitle").next_siblings:
        if char.name == "div":
            break
        else:
            author_birth_place += str(char)
    # print(author_birth_place)
    birth_country_stripped = author_birth_place.strip().split(",")[-1]
    birth_country_stripped_1 = birth_country_stripped.strip()
    data_birth_country = birth_country_stripped_1.split("\n")[0].strip()
    if data_birth_country[0:3] == "The":
        data_birth_country = data_birth_country[4:].strip()
    elif data_birth_country[0:6] == "in The":
        data_birth_country = data_birth_country[7:].strip()
    elif data_birth_country[0:2] == "in":
        data_birth_country = data_birth_country[3:].strip()
    elif data_birth_country == "":
        data_birth_country = "N/A"
    collections.insert_one({"title" : data_title, "author" : data_author, "birth_country" : data_birth_country, "current_readers" : data_book_currently_reading, "ratings_number" : data_book_ratings, "book_year": data_book_year})
