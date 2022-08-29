from threading import Thread
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs
import utils.misc as msg
from utils.requestclass import CheckImgExtension, CheckStatusCode, IsValid, get_all_images_new, get_all_images_thread

from utils.utils import progressbar as progbar

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

    def append_new_list(self):
        self.lists_of_lists.append([])
    
    def append_new_img_list(self):
        self.lists_of_images.append([])

    def set_list_of_lists(self, lvl):
        if lvl == 0:
            self.lists_of_lists.append([])
            return
        for i in range(lvl):
            self.lists_of_lists.append([])
    

    def set_list_of_images(self, lvl):
        if lvl == 0:
            self.lists_of_images.append([])
            return
        for i in range(lvl):
            self.lists_of_images.append([])
    

    def set_base_level(self, url):
        """Sets the head list of lists."""
        hrefs = []
        hrefs = obtain_base_href(url)
        with open('log/logfile-set_base_level_0', 'w') as f:
            for h in hrefs:
                f.write(h)
                f.write('\n')
                self.lists_of_lists[1].append(h)
            hrefs.clear()
    

    def set_base_level_images(self, pathname, urlList):
        """Sets the head list of lists with the images url."""
        print(f'{msg.INFO} urlList in base_level_images: {urlList}')
        with open('log/logfile-set_base_level_img_0', 'w') as f:
            imgs = []
            imgs = get_base_images(pathname, urlList)
            print(f'{msg.INFO} imgs in base_level_images: {imgs}')
            for h in imgs:
                f.write(h)
                f.write('\n')
                self.lists_of_images[1].append(h)
        imgs.clear()


    def set_level_list_images(self, lst, pos):
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
    
    def get_base_level(self):
        for l in self.get_list_of_lists():
            return l
    
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
    

    def set_level(self, lev):
        self.level = lev

    def get_level(self):
        return self.level

    def get_visited(self):
        return self.visited
    
    def remove_from_stack_and_add_to_visit(self):
        """ Pops first `url` of stack and appends it to visited."""
        p = self.stack.pop(0)
        self.visited.append(p)
    
    def add_to_stack(self, url):
        """ Adds `url` at the head of list."""
        self.stack.insert(0, url)

    def pop_item(self):
        p = self.stack.pop(0)
        return p

    def add_to_visited(self, url):
        """ Adds `url` at the end of list."""
        self.visited.append(url)



def obtain_all_href(url, auxList):
    """
    Appends to `auxList` all hrefs obtained from `urls`

    Return: `auxList` of extracted urls
    """

    #auxList = []
    #for url in progbar(urls, 'Obtaining hrefs: '):
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
    #return auxList

def obtain_base_href(url):
    """
    Returns all hrefs obtained from `url`
    """
    auxList = []
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
    return auxList

def get_base_images(pathname, url):
    """
    Return list all images(jpg, jpeg, gif, bmp) URLs on a `url` array
    """
    print(f'{msg.INFO} Url in get all img new: {url}')
    imgList = []
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
                if check_format in imgList:
                    if IsValid(img_url):
                        imgList.append(check_format)
    return imgList