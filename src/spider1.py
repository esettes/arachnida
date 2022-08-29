#!/usr/bin/python3
from concurrent.futures import ThreadPoolExecutor
from locale import currency
from threading import Thread
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
import requests
from utils.utils import SetArgs, progressbar as progbar
from utils.requestclass import CheckImgExtension, CheckStatusCode, IsValid, Spider, get_all_images_new
from utils.listsurlclass import URLlists, get_base_images, obtain_all_href, obtain_base_href
import utils.misc as msg
from utils.checker import download, download2
from multiprocessing import cpu_count

#import ipdb
#ipdb.set_trace()
#ipdb.set_trace(context=6)

url_threads = []
img_threads = []
download_threads = []

def	main():
    # get the number of cpu cores
    num_cores = cpu_count()
    # report details
    print(f'{msg.INFO}Num cores: {num_cores}')
    start_time = time.time()
    url = ""
    args = SetArgs()
    levelTo = 0
    spider = Spider()
    currLevel = 0
    urlLists = URLlists()

    
    #spider.set_pathname(path_)
    if args.path != 'data':
        spider.set_pathname(args.path)
    if args.recursive and args.level == 0:
        spider.set_url(args.recursive)
    if args.recursive and args.level != 0:
        spider.set_url(args.recursive)
        spider.set_level(args.level)

    urlLists.append_new_list()
    urls = obtain_base_href(spider.get_url())
    urlLists.set_level_list(urls, 0)

    urlLists.append_new_img_list()
    imgs = get_base_images(spider.get_pathname(), spider.get_url())
    urlLists.set_level_list_images(imgs, 0)

    if currLevel < spider.get_level():
        currLevel += 1
        nxtLevel = currLevel
        time.sleep(0.5)
        recursive_obtain_urls(nxtLevel, urlLists, spider, urls)
        time.sleep(0.5)
        recursive_obtain_imgs(currLevel, urlLists, spider, imgs)
    elif currLevel == spider.get_level():
        thread_submit(imgs, currLevel)

    with open('log/log_hrefs_list_1', 'a') as f:
        for h in urlLists.get_list_of_lists():
            for item in h:
                f.write(item)
                f.write('\n')
    
    with open('log/log_images_list_1', 'a') as f:
        for h in urlLists.get_lists_of_images():
            for item in h:
                f.write(item)
                f.write('\n')
    

    time.sleep(0.5)
    print(msg.DONE)
    print("--- %s seconds ---" % (time.time() - start_time))
    return


def recursive_obtain_urls(currLevel, urlLists, spider, urls):

    while currLevel <= spider.get_level():
        print(f'{msg.INFO}Current level: [{currLevel}]')
        u = []
        urlLists.append_new_list()

        for url in progbar(urls, msg.OBATAIN_URLS):
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


def recursive_obtain_imgs(currLevel, urlLists, spider, imgs):

    thread_submit(imgs, currLevel)
    while currLevel <= spider.get_level():
        im = []
        urlLists.append_new_img_list()
        for url in progbar( urlLists.get_list_of_lists()[currLevel], msg.RECOLECT_IMG):
            threadImgs = Thread(target=get_all_images_new, args=(spider.get_pathname(), url, im))
            threadImgs.start()
            img_threads.append(threadImgs)
        
        for t in img_threads:
            t.join()
        urlLists.set_level_list_images(im, currLevel)

        currLevel += 1
        recursive_obtain_imgs(currLevel, urlLists, spider, im)
    return

def thread_submit(urls, lvl):
    with ThreadPoolExecutor(10) as executor:
        with open('log/logimg_1', 'a') as myf:
            for img in progbar(urls, "[" + str(lvl) + "] " + msg.DOWNLOAD):
                print(f'{msg.URL} {img}')
                f = executor.submit(download, img)
                img_name = img.rsplit('/', 1)[-1]
                myf.write(img_name + '\n')


if __name__ == '__main__':
	main()