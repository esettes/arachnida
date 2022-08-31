import requests
import os
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

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

def CheckStatusCode(url):
	"""Return `True` if success request, and `False` if fails"""
	status = url.status_code
	if status >= 200 and status < 300:
		return True
	#msg.status_msg(str(status))
	return False

def CheckURLFormat():
	#Check what king of url inputs user
	print("OK")

def get_all_images_new(pathname, url, imgList):
	"""
	Appends to `imgList` all images(jpg, jpeg, gif, bmp) founded in `url`
	"""
	with open('log/logfile-new_img_0', 'w') as f:
		getURL = requests.get(url)
		if CheckStatusCode(getURL) != False:
			soup = bs(getURL.content, "lxml")
			all = soup.find_all("img")
			#print (all)

			for img in all:
				try:
					img_url = img.attrs.get("src")
				except:
					pass
				try:
					img_url = img.attrs.get("data-src")
				except:
					pass
				#temp = img_url
				#net = urlparse(temp)
				#if net.netloc == main_url:
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
					if not check_format in imgList:
						if IsValid(img_url):
							imgList.append(check_format)
							f.write(img_url + '\n')


def FormatUrlWithHttp(url):
	# Apply url._replace(scheme='http') if in input is not set
	url._replace(scheme='http')

