#!/usr/bin/python3.9
import requests
from bs4 import BeautifulSoup


def	main():
	URL = "https://realpython.github.io/fake-jobs/"
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.find(id="ResultsContainer")
	print(results.prettify())

if __name__ == '__main__':
	main()