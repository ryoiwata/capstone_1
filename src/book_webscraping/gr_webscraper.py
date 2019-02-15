import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
# Create instance of the MongoClient class
client = MongoClient()
database = client['capstone_1_db']   # Database name (to connect to)
collections = database['good_reads_best_books'] # Collection name (to use)

for num in range(1,11):
    print(num)
    pg_num = num
    gr_webpage = requests.get('https://www.goodreads.com/list/show/1.Best_Books_Ever?page={}'.format(pg_num))
    soup = BeautifulSoup(gr_webpage.text, 'html.parser')

    book_index = 0
    for obj in soup.findAll('tr',itemtype='http://schema.org/Book'):
        try:
            book_obj = obj.find('a',class_='bookTitle')
            book_title = obj.find('a',class_='bookTitle').text
            data_title = str(book_title).split("(")[0].strip()
            print(data_title)

            link_book = "https://www.goodreads.com" + book_obj["href"]
            # print(link_book)

            book_ratings = obj.find('span',class_='stars staticStars')
            rating = ""
            for char in book_ratings.next_siblings:
                if char.name == "span":
                    break
                else:
                    rating = char
            book_rating_avg_num = rating.strip().split("—")
            data_avg_rating = float(book_rating_avg_num[0].strip().split()[0])
            num_rating = book_rating_avg_num[1].strip().split()[0]
            data_num_rating = int("".join(num_rating.split(",")))
            # print(data_avg_rating)
            # print(data_num_rating)


            book_votes = soup.find_all("a", {"id" : lambda L: L and L.startswith('loading')})[book_index]
            # book_votes = obj.find('a',id='loading_link_564558')
            book_num_votes = book_votes.text.split()[0]
            data_book_num_votes = int("".join(book_num_votes.split(",")))
            print(data_book_num_votes)
            book_index += 1

            book_sub_page = requests.get(link_book)
            book_sub_soup = BeautifulSoup(book_sub_page.text, 'html.parser')

            try:
                book_year = book_sub_soup.find("nobr", class_ = "greyText")
                data_book_year = int(book_year.text.strip().split()[-1][:-1])
                # print(data_book_year)

            except:
                book_year = book_sub_soup.find_all("div", class_ = "row")[1]
                book_year_date = book_year.text.strip().split("\n")[1]
                data_book_year = int(book_year_date.split()[-1])
                # print(data_book_year)

            book_genre = book_sub_soup.find("a", class_ = "actionLinkLite bookPageGenreLink")
            data_book_genre = book_genre.text.strip()
            # print(data_book_genre)


            author_names = obj.find_all('span',itemprop='name')[1]
            data_author = author_names.text.strip()
            # print(data_author)

            author_link = obj.find("a", class_ = "authorName")
            link_author = author_link["href"]
            # print(link_author)

            author_sub_page = requests.get(link_author)
            # print(link_author)
            author_sub_soup = BeautifulSoup(author_sub_page.text, 'html.parser')
            author_birth_place = ""
            try:
                for char in author_sub_soup.find("div", class_ = "dataTitle").next_siblings:
                    if char.name == "div":
                        break
                    else:
                        author_birth_place += str(char)
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
            except:
                data_birth_country = "N/A"
            collections.insert_one({"title" : data_title,"author" : data_author, "birth_country" : data_birth_country, "genre": data_book_genre, "average_rating": data_avg_rating, "number_of_ratings": data_num_rating, "book_year": data_book_year, "votes": data_book_num_votes})

        except:
            pass
    # print(data_birth_country)
