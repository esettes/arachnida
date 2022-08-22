#!/usr/bin/python3
from distutils.command.clean import clean
from threading import Thread
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
	cleanList = []
	#spider.set_pathname(path_)
	if args.path != 'data':
		print(f'{msg.BLUEAQUA}press new path: {args.path}')
		spider.set_pathname(args.path)
	if args.recursive and args.level == 0:
		# check if is valid link here(?)
		spider.set_url(args.recursive)
		#spider.set_url(url)
	if args.recursive and args.level != 0:
		spider.set_url(args.recursive)
		#spider.set_url(url)
		spider.set_level(args.level)
	
	get_all_images2(spider)

	#Threads
	#for stac in spider.get_stackURLs():
	#	cleanList.append(CleanURLToQueue(stac))
#	thread = Thread(target=download, args=(cleanList, spider.get_pathname()))
#	thread.start()
	# wait for the task to complete
#	thread.join()

	#Threadpool map
	with ThreadPoolExecutor(10) as executor:
		e = executor.map(download, spider.get_stackURLs())
		count = list(e)
		for i in progbar(count, msg.DOWNLOAD):
			r = 'main: results: {}'.format(e)
	#extractedURLs = get_level_urls(url)
	#for ext in extractedURLs:
	#	print(ext)
	#try:
	count = 0
	# ThreadPool
	#with ThreadPoolExecutor(10) as executor:
	#	for img in progbar(spider.get_stackURLs(), msg.DOWNLOAD):
	#		executor.submit(download, img)
	#		#time.sleep(0.01)
	
	print(msg.DONE)
	print("--- %s seconds ---" % (time.time() - start_time))
	return






def WriteInNewFile(filepath, content_):
	with open(filepath, "w") as f:
		f.write(content_)

def ExtractURLs(filepath, soup):
	with open("content_prettify3.txt", "w") as f:
		for link in soup.find_all('a'):
			f.writelines(link.get('href'))



if __name__ == '__main__':
	main()
	

