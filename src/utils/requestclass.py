import requests
import os
import sys
#from utils.checker import download, get_all_images
import utils.misc as msg
import concurrent.futures
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from utils.utils import progressbar as progbar


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
		self.img_URLs = []

	
	def set_level(self, lev):
		self.levelTo = lev
	
	def set_url(self, u):
		self.url = u

	def set_pathname(self, p):
		path_ = self.CreateDownloadFolder(p)
		if path_ != None:
			self.pathname = path_

	def get_level(self):
		return self.levelTo

	def get_url(self):
		return self.url

	def get_pathname(self):
		return self.pathname
	
	def set_stackURLs(self, mylist):
		self.stack_URLs = mylist

	def get_stackURLs(self):
		return self.stack_URLs

	def add_to_stack(self, url):
		""" Adds `url` to stack."""
		self.stack_URLs.append(url)
	
	def add_img_url(self, url):
		""" Adds `url` to stack."""
		self.img_URLs.append(url)
	
	def get_img_URLs(self):
		return self.img_URLs




	def CreateDownloadFolder(self, pathname):
		if not os.path.isdir(pathname):
			os.makedirs(pathname)
		return pathname



def IsValid(url):
	"""
	Checks whether `url` is a valid URL. Check netloc(domain name)
	and squeme(protocol) are there.
	"""
	parsed = urlparse(url)
	#if bool(parsed.netloc) and bool(parsed.scheme):
		#print(f'{msg.ORANGEDARK} Parse: {msg.END}{msg.GREY246}{parsed}{msg.END}')
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
	msg.status_msg(str(status))
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

def get_all_images_thread(pathname, stackURLs, imgList):
	"""
	Returns all valid images(jpg, jpeg, gif, bmp) URLs on a `url` array
	"""
	for url in progbar(stackURLs, 'Process-2: '):
		getURL = requests.get(url)
		if CheckStatusCode(getURL) != False:
			soup = bs(getURL.content, "lxml")
			all = soup.find_all("img")
			for img in all:
				img_url = img.attrs.get("src")
				if not img_url:
					continue
				img_url = urljoin(url, img_url)
				try:
					pos = img_url.index("?")
					img_url = img_url[:pos]
				except ValueError:
					pass
				if CheckImgExtension(img_url):
					
					check_format = img_url + '/' + str(pathname)
					#print(f'check formnat: {check_format} and img_url: {img_url}')
					if not check_format in stackURLs:
						if IsValid(img_url):
							imgList.append(check_format)

def get_all_images2(object):
	"""
	Returns all valid images(jpg, jpeg, gif, bmp) URLs on a `url` array
	"""
	for url in progbar(object.get_stackURLs(), msg.PURPLEDARK + 'Obtaining img links: '):
		getURL = requests.get(url)
		if CheckStatusCode(getURL) != False:
			soup = bs(getURL.content, "lxml")
			all = soup.find_all("img")
			for img in all:
				img_url = img.attrs.get("src")
				if not img_url:
					continue
				img_url = urljoin(url, img_url)
				try:
					pos = img_url.index("?")
					img_url = img_url[:pos]
				except ValueError:
					pass
				if CheckImgExtension(img_url):
					check_format = img_url + '/' + str(object.get_pathname())
					if not check_format in object.get_stackURLs():
						if IsValid(img_url):
							object.add_img_url(check_format)

def FormatValidUrl(url):
	# Apply url._replace(scheme='http') if in input is not set
	url._replace(scheme='http')