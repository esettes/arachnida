#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from utils.requestclass import Spider
from utils.checker import download
from utils.checker import get_all_images
from utils.progressbar import progressbar as progbar
import utils.misc as msg

def	main():
	url = 'https://github.com/rsalmei/alive-progress'
	url = 'https://github.com/trinib/trinib'
	path_ = "img_folder8"
	args = ''
	levelTo = 0
	pathToSaveImgs = ''
	inputURL = ''
	#spider = Spider(0, path_)
	imgs = get_all_images(url)

	for img in progbar(imgs, msg.DOWNLOAD):
		download(img, path_)
	print(msg.DONE)



def WriteInNewFile(filepath, content_):
	with open(filepath, "w") as f:
		f.write(content_)

def ExtractURLs(filepath, soup):
	with open("content_prettify3.txt", "w") as f:
		for link in soup.find_all('a'):
			f.writelines(link.get('href'))



if __name__ == '__main__':
	main()

