#!/usr/bin/python3
from threading import Thread
from urllib.parse import urlparse
import requests
import time
from bs4 import BeautifulSoup as bs
from utils.requestclass import CheckStatusCode, IsValid, Spider, get_all_images2, CleanURLToQueue, get_all_images_thread
from utils.listsurlclass import URLlists
from utils.checker import download
from utils.utils import SetArgs, progressbar as progbar, set_log
import utils.misc as msg
from concurrent.futures import ThreadPoolExecutor
from utils.threadclass import CustomThread
import warnings
def	main():
	start_time = time.time()
	url = ""
	args = SetArgs()
	levelTo = 0
	inputURL = ''
	spider = Spider(levelTo, url)
	
	#spider.set_pathname(path_)
	if args.path != 'data':
		spider.set_pathname(args.path)
	if args.recursive and args.level == 0:
		# check if is valid link here(?)
		spider.set_url(args.recursive)
		#spider.set_url(url)
	if args.recursive and args.level != 0:
		spider.set_url(args.recursive)
		#spider.set_url(url)
		spider.set_level(args.level)
	temp = ObtainAllHref(spider.get_url(), spider.get_level())

	for t in temp:
		spider.add_to_stack(t)
	#for url in spider.get_stackURLs():#progbar(spider.get_stackURLs(), msg.RECOLECT_IMG):
	#	spider.set_url(url)
	#	countAllImg += get_all_images2(spider)
	time.sleep(0.1)

	warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
	#myThread = CustomThread(spider)
	tempList = []
	threadGetImages = Thread(target=get_all_images_thread, args=(spider.get_pathname(), spider.get_stackURLs(), tempList))
	#myThread.start()
	threadGetImages.start()
	
	#myThread.join()
	threadGetImages.join()
	print("--- %s seconds ---" % (time.time() - start_time))
	start_time1 = time.time()
	

	thread_submit(tempList)
	#for img in progbar(tempList, msg.DOWNLOAD):
	#	download(img)
	
	msg.info_msg("\nFinishing...\n")
	time.sleep(0.5)
	print(msg.DONE)
	print("--- %s seconds ---" % (time.time() - start_time1))
	return

def ObtainAllHref(inputURL, level):
	currentLevel = -1
	count = 0
	countAll = 0
	net = urlparse(inputURL)
	main_url = net.netloc
	print(f'{msg.YELLOW}{main_url} {msg.END}')
	uList = URLlists()
	uList.add_to_visited(inputURL)

	with open('log/logfile_3', 'w') as f:
		for v in uList.get_visited():#progbar(uList.get_visited(), 'Obtaining URLs: '):
			currentLevel += 1
			#print(f'{msg.INFO}Current level: {currentLevel}')
			try:
				req = requests.get(v)
				if CheckStatusCode(req) == False:
					print(msg.GREY246 + req)
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
						if g not in uList.get_visited():
							if IsValid(g):
								#print(g)
								uList.add_to_visited(g)
								f.write('[' + str(level) + '] ' + '[VISIT]' + ': ' + g + '\n')
				print(f'{msg.INFO}Finish URLs extraction.')
				print(f'{msg.GREY246}Removed {countAll - count} hrefs, parsed {len(uList.get_visited())} hrefs.')
				return uList.get_visited()
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
					if g not in uList.get_stack():
						if IsValid(g):
							#print(g)
							uList.add_to_stack(g)
							f.write('[' + str(level) + '] ' + '[S]' + ': ' + g + '\n')
			#if len(uList.get_visited()) + 1 > len(uList.get_visited()):
			#	continue
			
			uList.remove_from_stack_and_add_to_visit()

		print(f'{msg.INFO} Finish URLs extraction.')
		print(f'{msg.GREY246}Removed {countAll - count} hrefs, parsed {len(uList.get_visited())} hrefs.')
		#return uList.get_visited()

def thread_submit(urls):
	with ThreadPoolExecutor(10) as executor:
		with open('log/logimg_0', 'w') as myf:
			for img in progbar(urls, msg.DOWNLOAD):
				f = executor.submit(download, img)
				beforename =  img.rsplit('/', 1)[-2]
				img_name = beforename.rsplit('/', 1)[-1]
				myf.write(img_name + '\n')
				#if as_completed(f):
				#	print("")
	

def thread_map(stackURLs):
	with ThreadPoolExecutor(6) as executor:
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
	

