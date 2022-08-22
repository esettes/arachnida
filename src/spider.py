#!/usr/bin/python3
from distutils.command.clean import clean
from pickle import EMPTY_LIST
from threading import Thread, main_thread
from urllib.parse import urlparse
from xml.dom.minicompat import EmptyNodeList
import requests
import time
from bs4 import BeautifulSoup as bs
from utils.requestclass import CheckStatusCode, IsValid, Spider, get_all_images2, CleanURLToQueue
from utils.listsurlclass import URLlists
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
		print(f'{msg.BLUEAQUA}press new url: {args.recursive}')
		spider.set_url(args.recursive)
		#spider.set_url(url)
	if args.recursive and args.level != 0:
		spider.set_url(args.recursive)
		#spider.set_url(url)
		spider.set_level(args.level)
	

	ObtainAllHref(spider.get_url(), spider.get_level())
	get_all_images2(spider)

	
	#extractedURLs = get_level_urls(url)
	#for ext in extractedURLs:
	#	print(ext)
	thread_submit(spider.get_stackURLs())
	#thread_map(spider.get_stackURLs())
	#try:
	count = 0
	# ThreadPool
	
	
	print(msg.DONE)
	print("--- %s seconds ---" % (time.time() - start_time))
	return

def ObtainAllHref(inputURL, level):
	currentLevel = -1
	count = 0
	countAll = 0
	net = urlparse(inputURL)
	main_url = net.netloc
	print(f'{msg.YELLOW} {main_url} {msg.END}')
	uList = URLlists()
	uList.add_to_visited(inputURL)

	for v in uList.get_visited():#progbar(uList.get_visited(), 'Obtaining URLs: '):
		currentLevel += 1
		try:
			req = requests.get(v)
			if CheckStatusCode(req) == False:
				print("")
		except Exception:
			pass
		if req.status_code < 300:	
			soup = bs(req.content, "lxml")
			hrefs = soup.find_all('a')
			countAll += len(hrefs)
		if currentLevel >= level:
			# put all urls in visited list and exit
			for h in hrefs:
				g = h.get('href')
				temp = g
				net = urlparse(temp)
				if net.netloc == main_url:
					try:
						pos = g.index("?")
						g = g[:pos]
					except Exception:
						pass
					try:
						pos = g.index("#")
						g = g[:pos]
					except Exception:
						pass
					if not g in uList.get_visited():
						if IsValid(g):
							count += 1
							uList.add_to_visited(g)
			print(f'{msg.INFO} Finish URLs extraction.')
			print(f'{msg.GREY246}Removed {countAll - count} hrefs, parsed {count} hrefs.')
			return
		for h in hrefs:#progbar(hrefs, 'Obtaining level ' + str(currentLevel) + ': '):
			g = h.get('href')
			temp = g
			net = urlparse(temp)
			if net.netloc == main_url:
				try:
					pos = g.index("?")
					g = g[:pos]
				except Exception:
					pass
				try:
					pos = g.index("#")
					g = g[:pos]
				except Exception:
					pass
				if not g in uList.get_stack():
					if IsValid(g):
						count += 1
						uList.add_to_stack(g)
		try:
			uList.remove_from_stack_and_add_to_visit()
		except Exception:
			break
	print(f'{msg.INFO} Finish URLs extraction.')
	print(f'{msg.GREY246}Removed {countAll - count} hrefs, parsed {count} hrefs.')

def thread_submit(stackURLs):
	with ThreadPoolExecutor(10) as executor:
		for img in progbar(stackURLs, msg.DOWNLOAD):
			f = executor.submit(download, img)
			#if as_completed(f):
			#	print("")
			#time.sleep(0.01)

def thread_map(stackURLs):
	with ThreadPoolExecutor(10) as executor:
		e = executor.map(download, stackURLs)
		count = list(e)
		for i in progbar(count, msg.DOWNLOAD):
			r = 'main: results: {}'.format(e)

def thread_target(pathname, stackURLs):
	cleanList = []
	for stac in stackURLs:
		cleanList.append(CleanURLToQueue(stac))
	thread = Thread(target=download, args=(cleanList, pathname))
	thread.start()
	# wait for the task to complete
	thread.join()

def WriteInNewFile(filepath, content_):
	with open(filepath, "w") as f:
		f.write(content_)

def ExtractURLs(filepath, soup):
	with open("content_prettify3.txt", "w") as f:
		for link in soup.find_all('a'):
			f.writelines(link.get('href'))



if __name__ == '__main__':
	main()
	

