from threading import Thread
from time import sleep
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs
from utils.utils import progressbar as progbar

from utils.requestclass import CheckImgExtension, CheckStatusCode, IsValid

# custom thread to obtain the valid image urls and append it to a list
class CustomThread(Thread):
    # constructor
    def __init__(self, object):
        # execute the base constructor
        Thread.__init__(self)
        self.value = None
        self.spider = object
        self.img_list = []
    
    # function executed in a new thread
    def run(self):
        # block for a moment
        sleep(1)
        # store data in an instance variable
        self.value = 'Hello from a new thread'
        for url in progbar(self.spider.get_stackURLs(), 'Process-1: '):
            getURL = requests.get(url)
            if CheckStatusCode(getURL) != False:
                soup = bs(url, "lxml")
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
                        check_format = img_url + '/' + str(self.spider.get_pathname())
                        print(check_format)
                        if not check_format in self.spider.get_stackURLs():
                            if IsValid(img_url):
                                self.img_list.append(check_format)
        