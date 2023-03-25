from projet2g import get_categories_urls, \
    file_creation_by_category
from projet2image import scrape_pics


url_site = "http://books.toscrape.com"  # variable:
# url from webpage to scrape:

list_href_category_to_use = get_categories_urls(
    url_site)  # list of all categories' urls from
# the website

user_input = input('Please key in what you want: Data or Pics?')

if user_input == 'Data':
    for i in range(-1, 49):
        i += 1
        url_category = list_href_category_to_use[i]
        file_creation_by_category(url_category)
        # creation of all csv files
elif user_input == 'Pics':
    scrape_pics(url_site)
else:
    user_input = input(
        'Error: Please key in what you want: Data or Pics?')
    if user_input == 'Data':
        for i in range(-1, 49):
            i += 1
            url_category = list_href_category_to_use[i]
            file_creation_by_category(url_category)
            # creation of all csv files
    elif user_input == 'Pics':
        scrape_pics(url_site)
