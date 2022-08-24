from threading import Thread
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from utils.requestclass import CheckStatusCode, IsValid

class URLlists(): 
    """
    Manage the extracted URLs
    """
    def __init__(self):
        self.stack = []

        self.visited = []
        self.level = 0
    

    def set_level_list(self, lst):
        for h in lst:
            self.stack.append(h)

    def set_list_of_lists(self, lvl):
        for i in range(0, lvl):
            self.stack.append([])
    
    def set_base_level(self, url):
        hrefs = []
        hrefs = recursive_list(url)
        for h in hrefs:
            self.stack[0].append(h)
        hrefs.clear()
        
    def get_list_of_lists(self):
        return self.stack

    def set_level(self, lev):
        self.level = lev

    def get_level(self):
        return self.level

    def get_visited(self):
        return self.visited
    
    def get_stack(self):
        return self.stack
    
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


    
   

def recursive_list(url):
    auxList = []
    obtain_all_href(url, auxList)
    #myThread = Thread(target=obtain_all_href, args=(url, auxList))
    #myThread.start()
    #myThread.join()
    return auxList

def obtain_all_href(url, auxList):
    getURL = requests.get(url)
    #if CheckStatusCode(getURL) != False:
    soup = bs(getURL.content, "lxml")
    hrefs = soup.find_all("a")
    net = urlparse(url)
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