import requests
import re

URL = "https://www.goodreads.com/book/random"

while True:
	html_text = requests.get(URL).text

	# Rating Count
	bg_rating_count 	= html_text.find("<span class=\"value-title\" title=\"") + 33
	end_rating_count	= html_text.find("\" itemprop=\"ratingCount\">", bg_rating_count)
	rating_count 		= int(html_text[bg_rating_count : end_rating_count].replace(',', ''))

	if rating_count >= 30:
		if "<span itemprop=\"numberOfPages\">" in html_text:
			
			# Title
			bg_title	= html_text.find("<meta property=\"og:title\" content=\"") + 35
			end_title	= html_text.find("\"/>", bg_title)
			title = html_text[bg_title : end_title].replace("&amp;", '&')
			title = re.sub(r'\((.*)\)','', title)

			# Pages
			bg_pages	= html_text.find("<span itemprop=\"numberOfPages\">") + 31
			end_pages	= html_text.find(" page", bg_pages)
			pages 		= int(html_text[bg_pages : end_pages])

			# Rating
			bg_rating	= html_text.find("<span class=\"average\" itemprop=\"ratingValue\">") + 45
			end_rating	= html_text.find("</", bg_rating)
			rating		= float(html_text[bg_rating : end_rating])

			if pages != 0:
				print(title, pages, rating, sep='\t')
