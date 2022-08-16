#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import os
import bcolors as col


def	main():
	URL = "https://realpython.github.io/fake-jobs/"
	URL = 'https://realpython.com/'
	folder_ = "img_folder"
	req = requests.get(URL)

	soup = BeautifulSoup(req.text, "lxml")

	imgs = soup.findAll('img')
	ObtainImages(imgs, folder_)
	#results = soup.findAll('img')
	#WriteInNewFile('extracting_tests/req-text-lxml.txt', soup.get_text())

def ObtainImages(images, folder_name):
	count = 0

	for i, image in enumerate(images):
		try:
			img_link = image["data-srcset"]
		except:
			try:
				img_link = image["data-src"]
			except:
				try:
					img_link = image["data-fallback-src"]
				except:
					try:
						img_link = image["src"]
					except:
						pass
	try:
		r = requests.get(img_link).content
		try:
			r = str(r, 'utf-8')
		except UnicodeDecodeError:
			with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
				f.write(r)
			count += 1
	except:
		pass
	if count == len(images):
		print("All Images Downloaded!")
	else:
		print(f"Total {count} Images Downloaded Out of {len(images)}")



def WriteInNewFile(filepath, content_):
	with open(filepath, "w") as f:
		f.write(content_)

def ExtractURLs(filepath, soup):
	with open("content_prettify3.txt", "w") as f:
		for link in soup.find_all('a'):
			f.writelines(link.get('href'))


if __name__ == '__main__':
	main()

