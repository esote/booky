import argparse
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import os.path
import requests
import re
import sys
import time

URL = "https://www.goodreads.com/book/random"


def to_int(rating_count):
	# Return rating count as an int
	if isinstance(rating_count, int):
		return rating_count
	else:
		rating_count = rating_count.split()[0]
		if ',' in rating_count:
			return int(rating_count.replace(',', ''))
		return int(rating_count)


def format_title(book_title):
	"""
		Return formatted book title:
			"Actual Book Title! (Series identifier #3)" -> "Actual Book Title!"
			"History of 4D Fish Slapping [Silly, P4]" -> "History of 4D Fish Slapping"

		Along with CSV formatting
	"""
	book_title = ' '.join(book_title.split()).replace('&amp;', '&')
	book_title = re.sub(r'(\(|\[)(.*)(\)|\])', '', book_title)
	book_title = '"' + book_title.replace('"', '""') + '"'
	if book_title[-2:-1] == ' ':
		book_title = book_title[:-2] + '"'
	return book_title


def get_html_source(session):
	# Return html source
	html_source = session.get(URL).text
	return bs(html_source, 'lxml', parse_only=SoupStrainer(id="metacol"))


def get_book_rating_count(soup):
	# Return book rating count
	try:
		book_rating_count = soup.find('span', attrs={'class': 'value-title'}).get_text()
		return book_rating_count
	except AttributeError:
		# Attribute error, the rating count is missing
		return -1


def get_book_title(soup):
	# Return book title
	return soup.find('h1', attrs={'class': 'bookTitle'}).get_text()


def get_book_pages(soup):
	# Return book pages
	book_pages = soup.find('span', attrs={'itemprop': 'numberOfPages'}).get_text()
	if " pages" in book_pages:
		return book_pages.replace(' pages', '')
	elif " page" in book_pages:
		return book_pages.replace(' page', '')
	return book_pages


def get_book_rating(soup):
	# Return book rating
	return soup.find('span', attrs={'itemprop': 'ratingValue'}).get_text()


def main():
	# Command line parsing: verbosity, min rating, and required file path
	parser = argparse.ArgumentParser(description="Gather random book data from Goodreads and append it to a file in CSV format, \
until the program is manually closed or until a connection issue. I recommend having the CSV header: Title,Pages,Rating.",
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3],
		help="""specify verbosity level, default = 2
0 = no output
1 = continually print line count after appending to file
2 = after keyboard interrupt, print count of lines added since program start and program run time
3 = both verbosity options 1 and 2""", default=2)
	parser.add_argument("-mr", "--min-rating", type=int, default=30,
		help="specify the minimum accepted rating, default = 30")
	parser.add_argument("filepath", help="output file, only supports FULL path (no tilde, etc.)")
	args = parser.parse_args()

	FILE_PATH = args.filepath
	MIN_RATING_COUNT = args.min_rating

	try:
		if args.verbosity in (2, 3):
			start_time = time.time()
			with open(FILE_PATH, 'r') as file:
				init_filelength = sum(1 for _ in file)

		s = requests.Session()

		while True:
			soup = get_html_source(s)
			book_rating_count = get_book_rating_count(soup)

			if to_int(book_rating_count) >= MIN_RATING_COUNT:
				try:
					book_pages = get_book_pages(soup)
					book_title = format_title(get_book_title(soup))
					book_rating = get_book_rating(soup)
					# Re-check if file exists to catch deletion while program is running
					if book_pages != "0" and os.path.isfile(FILE_PATH):
						with open(FILE_PATH, 'a') as file:
							file.write(book_title + ',' + book_pages + ',' + book_rating + '\n')

						if args.verbosity in (1, 3):
							sys.stdout.write("\033[F")
							with open(FILE_PATH, 'r') as file:
								print("\nLine count:", sum(1 for _ in file), end='')
					elif not os.path.isfile(FILE_PATH):
						raise FileNotFoundError

				except AttributeError:
					continue

	except FileNotFoundError:
		print("File '", FILE_PATH, "' does not exist, or has been deleted.", sep='')

	except KeyboardInterrupt:
		if args.verbosity in (2, 3):
			with open(FILE_PATH, 'r') as file:
				lines_added = sum(1 for _ in file) - init_filelength
			print("\nLines added: ", lines_added, " (since program start)", sep='')
			print("Run time: ", round(time.time() - start_time, 3), " seconds (real)", sep='')

if __name__ == '__main__':
	try:
		main()

	except ConnectionResetError:
		print("\nConnection reset by peer, exiting program.")
		pass
