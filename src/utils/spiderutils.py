from concurrent.futures import ThreadPoolExecutor
from fileinput import close
import sys
from threading import Thread
import time
from utils.downloadimg import download
from utils.listsurlclass import obtain_all_href
import utils.misc as msg
import argparse
from pathlib import Path
from argparse import RawTextHelpFormatter

from utils.requestclass import get_all_images_new

url_threads = []
img_threads = []
download_threads = []


def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
    """
    Custom progress bar.
     Arguments: `it` Number of items; `prefix` Informative message near bar;
 `size` The size of th bar; `out` Output 
    """
    count = len(it)
    if count == 0:
        count = 1
    try:
        def show(j):
            x = int(size*j/count)
            print("{}[{}{}] {}/{}".format(prefix, msg.LOAD*x, msg.DOT*(size-x), j, count), # █
                   end='\r', file=out, flush=True)
    except Exception:
        pass
    show(0)
    try:
        for i, item in enumerate(it):
            yield item
            show(i+1)
    except Exception:
        pass
    print( flush=True, file=out)


def SetArgs():
    head = """  """
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description=head)
    group = parser.add_argument_group('Required argument')
    group.add_argument('-r','--recursive', type=str, metavar='URL', nargs='?', default=None, help="Download recursively images from passed URL.")
    parser.add_argument('-l','--level', type=int, metavar='LEVEL', nargs='?', const=5, default=0, choices=range(0,16), help="Depth level to \
download images from web, if not indicate flag, default is 0. \
If indicate flag but not set a value for it, the default val is 5")

    #excludeGroup = parser.add_mutually_exclusive_group()
    parser.add_argument('-p','--path', type=Path, metavar='PATH', default='data', help="Change the default path to store downloaded images. Thefault path is /data")
    args = parser.parse_args()
    return args

def set_log(listType, level, url):
    file = open('log/logfile_', 'r')
    lines = file.readlines()

    i = len(lines)
    s = 'L[' + str(level) + '] ' + listType + ': ' + url + '\n'
    lines[i + 1] = s
    with open('log/logfile_', 'w') as f:
    #if f.readline in ['\n', '\r\n']:
        f.writelines(lines)
        file.close
        return

def recursive_obtain_urls(currLevel, urlLists, spider, urls):

    while currLevel <= spider.get_level():
        print(f'{msg.INFO}Current level: [{currLevel}]')

        u = []
        urlLists.append_new_list()

        with open('log/log_hrefs_list_1', 'a') as f:
            for url in progressbar(urls, msg.OBATAIN_URLS):
                f.write(url)
                f.write('\n')
                threadHref = Thread(target=obtain_all_href, args=(url, u))
                threadHref.start()
                url_threads.append(threadHref)

        for t in url_threads:
            t.join()

        urlLists.set_level_list(u, currLevel)
        urls.clear()
        
        time.sleep(0.5)
        currLevel += 1
        recursive_obtain_urls(currLevel, urlLists, spider, u)
    return


def recursive_obtain_imgs(currLevel, urlLists, spider, imgs, main_url):

    thread_submit(imgs, currLevel)
    while currLevel <= spider.get_level():
        im = []
        urlLists.append_new_img_list()
        for url in progressbar( urlLists.get_list_of_lists()[currLevel], msg.RECOLECT_IMG):
            
            threadImgs = Thread(target=get_all_images_new, args=(spider.get_pathname(), url, im, main_url))
            threadImgs.start()
            img_threads.append(threadImgs)
        
        for t in img_threads:
            t.join()
        urlLists.set_level_list_images(im, currLevel, main_url)

        currLevel += 1
        recursive_obtain_imgs(currLevel, urlLists, spider, im, main_url)
    return

def thread_submit(urls, lvl):
    with ThreadPoolExecutor(10) as executor:
        with open('log/logimg_1', 'a') as myf:
            for img in progressbar(urls, "[" + str(lvl) + "] " + msg.DOWNLOAD):
                f = executor.submit(download, img)
                beforename =  img.rsplit('/', 1)[-2]
                img_name = beforename.rsplit('/', 1)[-1]
                myf.write(img_name + '\n')