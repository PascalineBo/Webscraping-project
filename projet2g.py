
import requests
from bs4 import BeautifulSoup
import csv
import re



def page_parser(url):
	"""retrieves and parses code from url page,
	using BeautifulSoup"""
	response = requests.get(url)
	page_html_code = response.content

	# transforms (parses) HTML into BeautifulSoup object:
	soup = BeautifulSoup(page_html_code, "html.parser")
	return soup


def get_categories_urls(category_url):
	"""
	:param category_url: page's category url
	:return: categories'urls from http://books.toscrape.com,
	in a list
	"""

	soup = page_parser(category_url)
	# extracts category's urls from "a" tags:
	a_href_url_category = soup.findAll(
		href=re.compile("^catalogue/category/books/"))  # beautiful
	# soup Resultset object

	list_href_category = []  # list to store all categories' urls

	for a in a_href_url_category:
		href_url_category = a['href']  # gives the extension
		# of the urls in Beautiful Soup Resultset object
		list_href_category.append(
			'http://books.toscrape.com/'+href_url_category)  # rebuilds
		# url's string and adds it to categories' urls list
	return list_href_category


def category_name(url_category):
	"""get category name from URL:"""
	split_url = url_category.split('/')
	categorys_name = split_url[6]
	return categorys_name


def category_all_pages_list(url_category_page1):
	"""get urls from all pages for one category,
	stores them in a list"""

	# reponse3 = requests.get(url_category1)

	list_urls_per_category=[]

	list_urls_per_category.append(url_category_page1)

	# listindex = [1,2,3,4,5,6,7,8]
	i=1

	while i in range(1, 10):
		i += 1
		url_next = url_category_page1.replace(
			'index', "page-"+str(i))
		response4 = requests.get(url_next)
		if response4.ok:
			list_urls_per_category.append(url_next)

	return list_urls_per_category


def get_all_books_from_category(category_url):
	"""get a list of books urls on each category page;
	:param category_url: category's page url
	"""
	page_books_urls = []  # list to store all books urls

	soup = page_parser(category_url)
	books_urls = soup.find_all("h3")  # get all book's urls
	# of the category listed in page's html code

	for h3 in books_urls:
		a_tag = h3.find('a')
		book_url = a_tag['href']
		clean_book_url = book_url.replace('../../../', "")
		# rebuilds a string with full book's page url
		page_books_urls.append(
			'http://books.toscrape.com/catalogue/' +
			clean_book_url)  # appends full book's url
		# to the list
	return page_books_urls


def book_details_urls(url_category):
	"""for one category, returns a list of urls of all
	the books from all the pages
	:param url_category: url from the first page of a category"""
	book_urls_list = []
	list_urls_per_category = category_all_pages_list(url_category)
	i = -1
	while i in range(-1, (len(list_urls_per_category)-1)):
		i += 1
		url = list_urls_per_category[i]
		page_books_urls = \
			get_all_books_from_category(url)
		book_urls_list += [*page_books_urls]  # concatenate lists of
	# books for all pages of the category
	return book_urls_list


def get_img_url(url):
	"""get the url of the image of a book"""
	soup = page_parser(url)
	img_tag = soup.find("img")
	partial_img_url = img_tag['src']
	img_url = ('http://books.toscrape.com' + (
		partial_img_url.replace('../..', "")))
	return img_url


def single_book_details(book_url):
	"""get book details"""
	soup = page_parser(book_url)

	book_info = [book_url]  # values list to
	# stash book details

	# find UPC:
	get_td = soup.find_all("td")  # get all  "td" data (text)
	td_content_list = []
	for content in get_td:
		td_content_list.append(content.string)

	book_info.append(td_content_list[0])  # stash UPC value

	title = soup.find("h1")  # get book title

	book_info.append(title.text)  # stash book title

	book_info.append(td_content_list[3])  # add Price
	# including Tax

	book_info.append(td_content_list[2])  # add Price
	# excluding Tax

	book_info.append(td_content_list[5])  # add Number
	# available

	# add Product Description:
	description = soup.find_all("p")
	product_description = []
	for desc in description:
		product_description.append(desc.string)

	book_info.append(product_description[3])

	a_tags_list = soup.find_all("a")  # get all "a" tags
	a_texts = []
	for category in a_tags_list:
		a_texts.append(category.string)

	book_info.append(a_texts[3])  # add category

	# add review rating:
	paragraphs = soup.find_all("p")
	p_texts = []
	for classe in paragraphs:
		p_texts.append(classe)

	tag = paragraphs[2]
	rating = tag['class']

	book_info.append(rating[1] + " stars")  # add
	# review rating

	book_info.append(get_img_url(book_url))  # append img_url:
	return book_info


def file_creation_by_category(url_category):
	"""for each category, creates a csv file with books data"""

	columns = ['product_page_url', 'universal_ product_code',
			   'title', 'price_including_tax',
			   'price_excluding_tax','number_available',
			   'product_description','category',
			   'review_rating','image_url']

	en_tete = ['product_data', 'content']
	with open(category_name(url_category)+'.csv', 'w',encoding='utf-8') as fichier_csv:
		writer = csv.writer(fichier_csv, delimiter=',')
		writer.writerow(columns)
		books_details_urls = book_details_urls(url_category)  # list
		# of all books'urls for one category
		for url in books_details_urls:
			writer.writerow(single_book_details(url))  # write
			# all the info for a book, on a row in the file
