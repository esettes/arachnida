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
	def __init__(self):
		self.url = ""
		self.levelTo = 0
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

def CleanURLToQueue(url):
	"""
	Removes the trick at the final of url and return `url` cleaned. 
	"""
	return url.rsplit('/', 1)[-2]

def CheckStatusCode(url):
	"""Return `True` if success request, and `False` if fails"""
	status = url.status_code
	if status >= 200 and status < 300:
		return True
	msg.status_msg(str(status))
	return False



def CheckURLFormat():
	#Check what king of url inputs user
	print("OK")

def get_all_images_thread(pathname, stackURLs, imgList):
	"""
	Returns all valid images(jpg, jpeg, gif, bmp) URLs on a `url` array
	"""
	print(msg.BLUELIGHT)
	print(stackURLs)
	with open('log/logfile-thread-2_5', 'w') as f:
		for url in progbar(stackURLs, 'Obtaining img links: '):
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
						if not check_format in stackURLs and not check_format in imgList:
							if IsValid(img_url):
								imgList.append(check_format)
								#stackURLs.append(check_format)
								f.write(img_url + '   ///////   with folder: ' + check_format +  '\n')

def get_all_images2(object):
	"""
	Returns all valid images(jpg, jpeg, gif, bmp) URLs on a `url` array
	"""
	with open('log/logfie-thread-1_0', 'w') as f:
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
								f.write(img_url + '\n')

def FormatValidUrl(url):
	# Apply url._replace(scheme='http') if in input is not set
	url._replace(scheme='http')