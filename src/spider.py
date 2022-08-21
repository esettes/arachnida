#!/usr/bin/python3
import requests
import time
from bs4 import BeautifulSoup
from utils.requestclass import Spider
from utils.checker import download, get_level_urls
from utils.checker import get_all_images
from utils.progressbar import progressbar as progbar
import utils.misc as msg
import concurrent.futures
from asyncio import Future
import asyncio
from typing import List

def	main():
	
	
	start_time = time.time()
	url = 'https://github.com/rsalmei/alive-progress'
	url = 'https://github.com/trinib/trinib'
	#url = 'https://realpython.github.io/fake-jobs/'
	path_ = "img_folder8"
	args = ''
	levelTo = 0
	pathToSaveImgs = ''
	inputURL = ''
	#spider = Spider(0, path_)
	
	imgs = get_all_images(url)
	#extractedURLs = get_level_urls(url)
	#for ext in extractedURLs:
	#	print(ext)
	threads = min(10, len(imgs))
	print(f'threads; {threads}')
	#for img in progbar(imgs, msg.DOWNLOAD):
	#	download(img, path_)
	try:
		with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
			res = executor.map(download, imgs)
			count = list(res)
			for i in progbar(count, msg.DOWNLOAD):
				r = 'main: results: {}'.format(res)
	except Exception:
		pass
	
	print(msg.DONE)
	print("--- %s seconds ---" % (time.time() - start_time))

def get_progress(futures: List[Future]) -> int:
    return sum([f.done() for f in futures])

def WriteInNewFile(filepath, content_):
	with open(filepath, "w") as f:
		f.write(content_)

def ExtractURLs(filepath, soup):
	with open("content_prettify3.txt", "w") as f:
		for link in soup.find_all('a'):
			f.writelines(link.get('href'))



if __name__ == '__main__':
	main()
	

