#!/usr/bin/python3
import requests
import time
from bs4 import BeautifulSoup
from utils.requestclass import Spider, get_all_images2, CleanURLToQueue
from utils.checker import download
from utils.utils import SetArgs, progressbar as progbar
import utils.misc as msg
from concurrent.futures import ThreadPoolExecutor
from asyncio import Future, as_completed
import asyncio
from typing import List

def	main():
	
	
	start_time = time.time()
	#url = 'https://github.com/rsalmei/alive-progress'
	url = 'https://github.com/trinib/trinib'
	#url = 'https://realpython.github.io/fake-jobs/'
	#path_ = "img_folder5" #default
	args = SetArgs()
	levelTo = 0
	inputURL = ''
	spider = Spider(levelTo, url)
	
	#spider.set_pathname(path_)
	if args.path != 'data':
		print(f'{msg.BLUEAQUA}press new path: {args.path}')
		spider.set_pathname(args.path)
	if args.recursive and args.level == 0:
		# check if is valid link here(?)
		#spider.set_url(args.recursive)
		spider.set_url(url)
	if args.recursive and args.level != 0:
		#spider.set_url(args.recursive)
		spider.set_url(url)
		spider.set_level(args.level)
	
	
	print(msg.GREENLIGHTBRIGHT)
	print("Spider object: " + msg.END)
	print('url: ' + spider.get_url())
	print(spider.get_pathname())
	print('level: ' + str(spider.get_level()))

	#return

	
	get_all_images2(spider)
	#imgs = get_all_images(spider, url)
	#extractedURLs = get_level_urls(url)
	#for ext in extractedURLs:
	#	print(ext)
	#try:
	count = 0
	with ThreadPoolExecutor(10) as executor:
		for img in progbar(spider.get_stackURLs(), msg.DOWNLOAD):
			executor.submit(download, img)
			time.sleep(0.01)
			print(msg.PINKDARK + 'THREADPOOL IMG: ' + img)
	

	#with ThreadPoolExecutor(10) as executor:
	#	res = executor.map(download, spider.get_stackURLs())
	#	count = list(res)
	#	for i in progbar(count, msg.DOWNLOAD):
	#		r = 'main: results: {}'.format(res)
	#except Exception:
	#	pass
	#for img in progbar(imgs, msg.DOWNLOAD):
	#	download(img, path_)
	#try:
	#	with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
	#		res = executor.map(download, imgs)
	#		count = list(res)
	#		print(msg.PURPLE)
	#		print(count)
	#		for i in progbar(count, msg.DOWNLOAD):
	#			r = 'main: results: {}'.format(res)
	#except Exception:
	#	pass
	
	print(msg.DONE)
	print("--- %s seconds ---" % (time.time() - start_time))







def WriteInNewFile(filepath, content_):
	with open(filepath, "w") as f:
		f.write(content_)

def ExtractURLs(filepath, soup):
	with open("content_prettify3.txt", "w") as f:
		for link in soup.find_all('a'):
			f.writelines(link.get('href'))



if __name__ == '__main__':
	main()
	

