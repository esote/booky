""" Thanks to Code Review user MrGrj! """

from bs4 import BeautifulSoup as bs
import requests
import re

URL = "https://www.goodreads.com/book/random"
MIN_RATING_COUNT = 30


def to_float(rating_count):
    """ Return rating count as a float """
    rating = rating_count.split()[0]
    if ',' in rating:
        return float(rating.replace(',', '.'))
    return float(rating)


def format_title(book_title):
    """ Return formatted book title """
    book_title = ' '.join(book_title.split()).replace('&amp;', '&')
    book_title = re.sub(r'(\(|\[)(.*)(\)|\])','', book_title)
    return book_title


def get_html_source():
    """ Return html source """
    html_source = requests.get(URL).text
    return bs(html_source, 'html.parser')


def get_book_rating_count(soup):
    """ Return book rating count """
    return soup.find('span', attrs={'class', 'value-title'}).get_text()


def get_book_title(soup):
    """ Return book title"""
    return soup.find('h1', attrs={'class': 'bookTitle'}).get_text()


def get_book_pages(soup):
    """ Return book pages """
    book_pages = soup.find('span', attrs={'itemprop': 'numberOfPages'}).get_text()
    if " pages" in book_pages:
        return book_pages.replace(' pages', '')
    elif " page" in book_pages:
        return book_pages.replace(' page', '')
    return book_pages


def get_book_rating(soup):
    """ Return book rating """
    return soup.find('span', attrs={'itemprop': 'ratingValue'}).get_text()


def main():
    """ Gather book data until the program is mainually closed. """
    while True:
        soup = get_html_source()
        book_rating_count = get_book_rating_count(soup)

        if to_float(book_rating_count) >= MIN_RATING_COUNT:
            try:
                book_pages = get_book_pages(soup)
                book_title = format_title(get_book_title(soup))
                book_rating = get_book_rating(soup)
                print(book_title, book_pages, book_rating, sep = '\t')
            except AttributeError:
                continue

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("You've decided to close the program")
