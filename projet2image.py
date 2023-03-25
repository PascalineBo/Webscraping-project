import requests
import os
from bs4 import BeautifulSoup
from projet2g import get_all_books_from_category, \
	get_categories_urls, page_parser, category_name


def get_img_url(book_url_2):
	"""get url from a picture of a book
	:param book_url_2: book's page url
	"""
	response_img = requests.get(book_url_2)
	page_img = response_img.content
	soup2 = BeautifulSoup(page_img, "html.parser")
	img_tag = soup2.find("img")
	partial_img_url = img_tag['src']
	img_url = ('http://books.toscrape.com'+(
		partial_img_url.replace('../..', "")))
	return img_url


cwd = os.getcwd()  # return current working directory


def scrape_pics(url_site):
	"""scrape all pictures from the website"""
	list_href_category_to_use = get_categories_urls(
		url_site)  # list of all categories' urls from
	# the website
	for url in list_href_category_to_use:
		category_name(url)
		list_of_books_urls = get_all_books_from_category(url)
		os.mkdir(category_name(url))  # create new category
		# directory with the name of the category
		os.chdir(category_name(url))  # navigate to new category
		# directory
		for book_url in list_of_books_urls:

			soup = page_parser(book_url)

			title = soup.find("h1")
			book_title = title.text  # get book title
			special_characters = ['(',')',' ',':',
								  'é',',','-','\'',
								  '?','*','\"']
			for c in special_characters:
				book_title = book_title.replace(c, '_')

			book_title = book_title[:30]  # limit the length of
			# book's picture title

			url_pic = get_img_url(book_url)  # get book pic url

			with open(r''+book_title+'_pic.jpg', 'wb') as handle:
				response = requests.get(url_pic, stream=True)

				if not response.ok:
					print(response)

				for block in response.iter_content(1024):
					if not block:
						break
					handle.write(block)
		os.chdir(cwd)  # navigate to parent directory
