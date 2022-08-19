import requests
import os
import utils.misc as msg
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from utils.progressbar import progressbar as progbar

class Spider(): 
	"""
	Main class for web scraping. 

	Arguments:
		`levelTo` Indicated by user, to which level scrap;
		`pathname` By default './data', but modifiyble by user;
		`imgs` Current level images(?maybe not need this public);
	"""
	def __init__(self, levelTo, pathname, imgs, url):
		self.levelTo = levelTo
		self.pathname = pathname
		self.imgs = imgs
		self.__levelURLs = [] # Saves the extracted hrefs of current level
		self.get_all_images(url)

	
	def set_level(self, lev):
		self.levelTo = lev
    
	def set_pathname(self, p):
		self.pathname = p

	def get_level(self):
		return self.levelTo
    
	def get_pathname(self):
		return self.pathname
	
	def set_levelURLs(self, url):
		# append to __levelURLs list all extracted level urls
		print('ok')

	def start_scrap(self):
		for url in self.__levelURLs:
			self.get_all_images(url)

	def get_all_images(self, url):
		"""
		Returns all valid images(jpg, jpeg, gif, bmp) URLs on a `url` array
		"""
		getURL = requests.get(url)
		msg.status_msg(str(getURL.status_code))
		soup = bs(getURL.content, "lxml")
		urls = []
		all = soup.find_all("img")
	
		for img in progbar(all, msg.RECOLECT_IMG):
			img_url = img.attrs.get("src")
			if not img_url:
				continue
			img_url = urljoin(url, img_url)
			# if url have key-value, remove all after '?'
			try:
				pos = img_url.index("?")
				img_url = img_url[:pos]
			except ValueError:
				pass
			if CheckImgExtension(img_url):
				if not img_url in urls:
					if IsValid(img_url):
						urls.append(img_url)
		msg.info_msg('Removed ' + str(len(all) - len(urls)) + ' images.')
		return urls

	def download(self, url, pathname):
		"""
		Downloads a file given an URL and puts it in the folder `pathname`
		"""
		if not os.path.isdir(pathname):
			os.makedirs(pathname)
		response = requests.get(url)
		img_name = url.rsplit('/', 1)[-1]
		with open(pathname + '/' + img_name, 'wb') as f:
			f.write(response.content)

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