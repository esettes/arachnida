import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs
from utils.requestclass import CheckStatusCode, IsValid
import utils.misc as msg


class URLlists(): 
    """
    Manage the extracted URLs
    """
    def __init__(self):
        self.lists_of_lists = []
        self.lists_of_images = []
        self.stack = []
        self.visited = []
        self.level = 0
    
    def append_new_list(self):
        self.lists_of_lists.append([])
    
    def append_new_img_list(self):
        self.lists_of_images.append([])

    def set_level_list(self, lst, pos):
        """Set the `lst` of the located list `pos` of the main list """
        i = 0
        with open('log/logfile-level_list_0', 'w') as f:
            for l in self.get_list_of_lists():
                if i == pos:
                    for h in lst:
                        f.write(h)
                        f.write('\n')
                        l.append(h)
                    return
                i += 1

    def set_level_list_images(self, lst, pos, main_url):
        """Set the `lst` of the list located in `pos`"""
        i = 0
        with open('log/logfile-set_level_lst_img_0', 'w') as f:
            for img_lst in self.get_lists_of_images():
                if i == pos:
                    for h in lst:
                        f.write(h)
                        f.write('\n')
                        img_lst.append(h)
                    return
                i += 1

    def get_list_of_lists(self):
        return self.lists_of_lists

    def get_lists_of_images(self):
        return self.lists_of_images
    
    def get_level(self, pos):
        i = 0
        for l in self.get_list_of_lists():
            if i == pos:
                return l
            i += 1
    
    def get_level_images(self, pos):
        i = 0
        for l in self.get_lists_of_images():
            if i == pos:
                return l
            i += 1

    def check_base_url(self, url, main_url):
        net = url
        net = urlparse(net)
        if main_url == net.netloc:
            return True
        return False

def obtain_all_href(url, auxList):
    """
    Appends to `auxList` all hrefs obtained from `urls`

    Return: `auxList` of extracted urls
    """

    getURL = requests.get(url)
    if CheckStatusCode(getURL) != False:
        soup = bs(getURL.content, "lxml")
        hrefs = soup.find_all("a")
        net = url
        net = urlparse(net)
        main_url = net.netloc
        
        for h in hrefs:
            g = h.get('href')
            #if CheckStatusCode(g):
            #    print(g)
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
                if g not in auxList:
                    if IsValid(g):
                        auxList.append(g)

