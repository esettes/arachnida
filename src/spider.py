#!/usr/bin/python3.9
import requests
from bs4 import BeautifulSoup
import os

def	main():
	URL = "https://realpython.github.io/fake-jobs/"
	page = requests.get(URL)

	soup = BeautifulSoup(page.content, "html.parser")
	results = soup.findAll('img')
	os.mkdir('img_folder')
	print(results.prettify())

	r = requests.get(URL).content
	with open("myfile.txt", "wb") as f:
		f.write(r)

if __name__ == '__main__':
	main()