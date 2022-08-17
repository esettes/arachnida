#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import utils.bcolors as col
from utils.checker import download
from utils.checker import get_all_images
from utils.utils import progressbar


def	main():
	URL = "https://realpython.github.io/fake-jobs/"
	URL = 'https://www.hola.com/belleza/20220816215154/recomendaciones-productos-sephora-celebrities/'
	url = 'https://github.com/rsalmei/alive-progress'
	path_ = "img_folder4"
	#req = requests.get(URL)

	#soup = BeautifulSoup(req.content, "lxml")

	#imgs = soup.findAll('img')
	
	#results = soup.findAll('img')
	#WriteInNewFile('extracting_tests/req-text-lxml.txt', soup.get_text())
	
	imgs = get_all_images(url)
	for img in imgs:
		# for each image, download it
		download(img, path_)
	#ObtainImages(imgs, folder_)

def ObtainImages(images, folder_name):
	count = 0
	i = 0
	for image in progressbar(range(len(images)), "Extracting images: ", len(images)):
		for image in images:#, progressbar(range(15), "Extracting images: ", 40):
			#img = image.get('src')
			#print(img)
			try:
				img_link = image["data-srcset"]
			except:
				try:
					img_link = image["data-src"]
				except:
					try:
						img_link = image["data-fallback-src"]
					except:
						try:
							img_link = image["src"]
						except:
							pass
		try:
			r = requests.get(img_link).content
			try:
				r = str(r, 'utf-8')
			except UnicodeDecodeError:
				with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
					f.write(r)
				count += 1
		except:
			pass
	if count == len(images):
		print("All Images Downloaded!")
	else:
		print(f"Total {count} Images Downloaded Out of {len(images)}")



def WriteInNewFile(filepath, content_):
	with open(filepath, "w") as f:
		f.write(content_)

def ExtractURLs(filepath, soup):
	with open("content_prettify3.txt", "w") as f:
		for link in soup.find_all('a'):
			f.writelines(link.get('href'))


if __name__ == '__main__':
	main()

