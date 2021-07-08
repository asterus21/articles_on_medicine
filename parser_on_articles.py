# TODO: parse https://www.nature.com/modpathol/articles?searchType=journalSearch&sort=PubDate&year=20{year}&page={page} where "page" equals the number of pages to go through and "year" is a year to find
#  there can be a different range for the "page" variable (see the year of publication)
#  so there is a need to get a list of pages to know the end of the range
#  get each link via <a>, itemprop="url", there'll be a list of links, each link should be appended to 'https://www.nature.com'
#  in order to parse all the articles check whether it's free-to-read, i.e. find id='access-option' in the html-code and if there is, pass the link
#  or you can get every link whether the article is free or not and mark those ones which are not free-to-read

import requests
from icecream import ic
from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator()

year = input()
url = f'https://www.nature.com/modpathol/articles?searchType=journalSearch&sort=PubDate&year={year}&page=1'
get_url = requests.get(url).text
making_soup = BeautifulSoup(get_url, 'lxml')

def get_the_number_of_links_to_pass():
	url = 'https://www.nature.com/modpathol/articles?searchType=journalSearch&sort=PubDate&year=2021&page=1'
	get_url = requests.get(url).text
	making_soup = BeautifulSoup(get_url, 'lxml')
	number_of_links = making_soup.find_all('li', class_='c-pagination__item')
	list_of_links = []
	for page in number_of_links:
		pages = page.get('data-page')
		list_of_links.append(pages)
	last_page = list_of_links[-2]
	ic(last_page)

get_the_number_of_links_to_pass()

def making_soup_of_the_year(soup_of_the_year): # fetching the list of links

	main_url_to_be_appended = 'http://www.nature.com'
	list_to_be_made = []
	links = soup_of_the_year.find_all('a', itemprop='url', href=True)
	for link_item in links:
		list_to_be_made.append(link_item['href'])
	final_list = [main_url_to_be_appended + item for item in list_to_be_made]

def get_text(link): # getting the text

	url = requests.get(link).text
	soup = BeautifulSoup(url, 'lxml')
	find_abstract = soup.find('div', id='Abs1-content')
	find_title = soup.find('h1', class_='c-article-title')
	abstract_to_text = find_abstract.get_text()
	title_to_text = find_title.get_text()

def translate(text_to_translate): # getting the translation

	translation = translator.translate(text_to_translate, dest='ru')
	string = str(translation)
	split_one = string.split('=')
	split_two = split_one[3]
	good_translation = split_two[:-15]

def the_fuck_I_know(): # getting a list of links where the articles are free-to-read or not free-to-read

	main_url_to_be_appended = 'http://www.nature.com'
	list_to_be_made = []
	links = making_soup.find_all('a', itemprop='url', href=True)
	for link_item in links:
		list_to_be_made.append(link_item['href'])
	final_list = [main_url_to_be_appended + item for item in list_to_be_made]
	for one_link_to_test in final_list:
		get_url_for_one_link_to_test = requests.get(one_link_to_test).text
		making_a_tasty_soup = BeautifulSoup(get_url_for_one_link_to_test, 'lxml')
		item_by_selector = making_a_tasty_soup.find_all('h2', id='access-options')
		