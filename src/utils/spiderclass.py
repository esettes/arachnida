import requests
import os
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import utils.misc as msg

class Spider(): 
	""" 
	Set the scrapper properties.
	"""
	def __init__(self):
		self.url = ""
		self.levelTo = 0
		self.pathname = ""
		self.main_url = ""
	
	def set_level(self, lev):
		self.levelTo = lev
	
	def set_url(self, u):
		if u[:3] == 'www':
			u = 'https://' + u
			self.url = u
		if u[:3] == 'www' and u[:4] == 'http':
			self.url = u
			return

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
	
	def set_base_url(self, url):
		net = url
		net = urlparse(net)
		self.main_url = net.scheme + '://' + net.netloc
	
	def get_main_url(self):
		return self.main_url


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


def get_all_images_new(pathname, url, imgList, main_url):
	"""
	Appends to `imgList` all images(jpg, jpeg, gif, bmp) founded in `url`
	"""
	if not os.path.isdir('log'):
			os.makedirs('log')
	with open('log/logfile-new_img_0', 'w') as f:
		getURL = requests.get(url)
		if CheckStatusCode(getURL) != False:
			soup = bs(getURL.content, "lxml")
			all = soup.find_all("img")

			for img in all:
				trigger = False
				try:
					img_url = img.attrs.get("src")
					img_url = img_url = FormatUrl(img_url, main_url)
					trigger = True
				except Exception:
					pass
				try:
					if trigger == False:
						img_url = img.attrs.get("data-src")
						img_url = FormatUrl(img_url, main_url)
				except Exception:
					pass
				if not img_url:
					continue
				try:
					pos = img_url.index("?")
					img_url = img_url[:pos]
				except ValueError:
					pass
				if CheckImgExtension(img_url):
					check_format = img_url + 'ñ' + str(pathname)
					if not check_format in imgList:
						if IsValid(img_url):
							imgList.append(check_format)
							f.write(img_url + '\n')


def FormatUrl(img_url, main_url):
	temp = img_url
	net = urlparse(temp)
	if net.netloc != main_url:
		if img_url[0] == '/':
			img_url = main_url + img_url
			return img_url
	return img_url
	# Apply url._replace(scheme='http') if in input is not set
	#url._replace(scheme='http')

def CheckBaseurl(url):
	if IsValid(url):
		try:
			getURL = requests.get(url)
		except Exception:
			msg.err_msg("URL doesn't exist.")
			return False
		try:
			if CheckStatusCode(getURL) == False:
				msg.err_msg("Bad status code.")
				return False
		except Exception:
			return False
	if IsValid(url) == False:
		print(url)
		msg.err_msg('Invalid URL. Check if you write it correctly and it starts with "www".')
		return False
	if not url:
		msg.err_msg('Invalid URL.')
		return False

	return True

