import requests
import os
import sys
#from utils.checker import download, get_all_images
import utils.misc as msg
import concurrent.futures
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from utils.utils import progressbar as progbar

"""
Spider urls dictionary. Obtain all level urls in a branched way.

e.

Dict = {} = obtain_level_ursl(url, levelTo)
	for key names use [level-number of url]
	e. if I have 3 urls in level 0 then their key-values are:
		{'0-0':'url-one',
		 '0-1':'url-two', 
		 '0-2':'url-three'}
	if my url-two have 2 urls then:
		['0-0':'url-one', '0-1':'url-two',, '0-2':'url-three']

print (Dict)

"""

class Spider(): 
	"""
	Main class for web scraping. 

	Arguments:
		`levelTo` Indicated by user, to which level scrap;
		`pathname` By default './data', but modifiyble by user;
		`imgs` Current level images(?maybe not need this public);
	"""
	def __init__(self, levelTo, url):
		self.url = url
		self.levelTo = levelTo
		self.pathname = ""
		#self.imgs = imgs
		self.status_code = 0
		self.stack_URLs = []	# imgs
		self.visited_URLs = []	#imgs
		self.queue_imgs = []
		self.__current_Level = 0
		self.__url_dictionary = {}
#		self.get_all_images(url)

	
	def set_level(self, lev):
		self.levelTo = lev
	
	def set_url(self, u):
		self.url = u
    
	def set_status_code(self, sc):
		self.status_code = sc

	def set_pathname(self, p):
		path_ = self.CreateDownloadFolder(p)
		if path_ != None:
			print(f'success!: {p}')
			self.pathname = path_

	def set_queue_imgs(self, urls):
		for q in urls:
			self.queue_imgs.append(CleanURLToQueue(q))
		print(f'queue: {self.queue_imgs}')
			

	def get_level(self):
		return self.levelTo

	def get_url(self):
		return self.url
	
	def get_status_code(self):
		return self.status_code

	def get_pathname(self):
		return self.pathname
	
	def get_stackURLs(self):
		return self.stack_URLs

	def get_visitedURLs(self):
		return self.visited_URLs

	def add_to_stack(self, url):
		""" Adds `url` at the head of stack."""
		self.stack_URLs.insert(0, url)
	
	def add_to_visited(self, url):
		""" Adds `url` at the end."""
		self.visited_URLs.append(url)

	def remove_from_stack_and_add_to_visit(self, url):
		""" Pops `url` of stack and appends it to visited."""
		p = self.stack_URLs.pop()
		self.visited_URLs.append(p)




	def CreateDownloadFolder(self, pathname):
	#pathname = "img_folder5"
		print(f'pathname: {pathname}')
		if not os.path.isdir(pathname):
			p = os.makedirs(pathname)
			print(f'pathname: {p}')
		return pathname




def IsValid(url):
	"""
	Checks whether `url` is a valid URL. Check netloc(domain name)
	and squeme(protocol) are there.
	"""
	parsed = urlparse(url)
	return bool(parsed.netloc) and bool(parsed.scheme)

def CheckImgExtension(f_name):
	if f_name.endswith('.gif') or f_name.endswith('.jpg') or \
		f_name.endswith('.jpeg') or f_name.endswith('.png') or \
			f_name.endswith('.bmp'):
				return True
	else:
		return False

def start_scrap(imgs):
	#imgs = get_all_images(url)
	threads = min(10, len(imgs))
	#for img in progbar(imgs, msg.DOWNLOAD):
	#	download(img, path_)
	try:
		with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
			res = executor.map(Spider.download, imgs)
			count = list(res)
			for i in progbar(count, msg.DOWNLOAD):
				r = 'main: results: {}'.format(res)
	except Exception:
		pass

def RecursiveSearch(object):
	currentLevel = 0
	if currentLevel <= object.get_level():
		#start get all hrefs
		print('ok')


def CleanURLToQueue(url):
	"""
	Removes the trick at the final of url and return `url` cleaned. 
	"""
	return url.rsplit('/', 1)[-2]

def CheckStatusCode(url):
	status = url.status_code
	if status >= 200 and status < 300:
		return True
	msg.bad_status_code(str(status))
	return False


def GetNodeURLs(url):
	"""
	Extracts the current level hrefs.

	Return:
		`hrefs` list
	"""
	getURL = requests.get(url)
	if CheckStatusCode(getURL) == False:
		return
	soup = bs(getURL.content, "lxml")
	hrefs = []
	all = soup.find_all('a')
	for h in progbar(all, msg.RECOLECT_HREF):
		obtain = h.get('href')
		if not obtain in hrefs:
			hrefs.append(obtain)
	msg.info_msg('Removed ' + str(len(all) - len(hrefs)) + ' hrefs.')
	return hrefs




def CheckURLFormat():
	#Check what king of url inputs user
	print("OK")

def get_all_images2(object):
	"""
	Returns all valid images(jpg, jpeg, gif, bmp) URLs on a `url` array
	"""
	print(f'get_url(): {object.get_url()}')
	getURL = requests.get(object.get_url())
	msg.status_msg(str(getURL.status_code))
	soup = bs(getURL.content, "lxml")
	all = soup.find_all("img")
	for img in progbar(all, msg.RECOLECT_IMG):
		img_url = img.attrs.get("src")
		if not img_url:
			continue
		img_url = urljoin(object.get_url(), img_url)
		# if url have key-value, remove all after '?'
		try:
			pos = img_url.index("?")
			img_url = img_url[:pos]
		except ValueError:
			pass
		if CheckImgExtension(img_url):
			if not img_url in object.get_stackURLs():
				if IsValid(img_url):
					img_url = img_url + '/' + str(object.get_pathname()) # ugly, sad
					object.add_to_stack(img_url)
	msg.info_msg('Removed ' + str(len(all) - len(object.get_stackURLs())) + ' images.')


