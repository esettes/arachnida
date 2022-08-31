#!/usr/bin/python3.9
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import time
import warnings
from utils.spiderutils import SetArgs, progressbar as progbar
from utils.requestclass import Spider, get_all_images_new, FormatUrl
from utils.listsurlclass import URLlists, obtain_all_href
import utils.misc as msg
from utils.downloadimg import download

#import ipdb
#ipdb.set_trace()
#ipdb.set_trace(context=6)

url_threads = []
img_threads = []
download_threads = []

def	main():
    start_time = time.time()
    args = SetArgs()
    spider = Spider()
    currLevel = 0
    urlLists = URLlists()

    if args.path != 'data':
        spider.set_pathname(args.path)
    if args.recursive and args.level == 0:
        spider.set_url(args.recursive)
    if args.recursive and args.level != 0:
        spider.set_url(args.recursive)
        spider.set_level(args.level)

    if not spider.get_url():
        print(spider.get_url())
        msg.err_msg('Invalid URL.')
        return

    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
    spider.set_base_url(spider.get_url())
    main_url = spider.get_main_url()

    url = spider.get_url()
    #spider.set_base_url(FormatUrl(url, ))


    #if spider.get_url() != 



    urls = []
    urlLists.append_new_list()
    obtain_all_href(spider.get_url(), urls)
    urlLists.set_level_list(urls, 0)

    imgs = []
    urlLists.append_new_img_list()
    get_all_images_new(spider.get_pathname(), spider.get_url(), imgs, main_url)
    urlLists.set_level_list_images(imgs, 0, main_url)

    if currLevel < spider.get_level():
        thread_submit(imgs, currLevel)
        currLevel += 1
        nxtLevel = currLevel
        recursive_obtain_urls(nxtLevel, urlLists, spider, urls)
        time.sleep(0.5)
        recursive_obtain_imgs(currLevel, urlLists, spider, imgs, main_url)
    elif currLevel == spider.get_level():
        thread_submit(imgs, currLevel)
    

    time.sleep(0.5)
    print(msg.DONE)
    print("--- %s seconds ---" % (time.time() - start_time))
    return


def recursive_obtain_urls(currLevel, urlLists, spider, urls):

    while currLevel <= spider.get_level():
        print(f'{msg.INFO}Current level: [{currLevel}]')

        u = []
        urlLists.append_new_list()

        with open('log/log_hrefs_list_1', 'a') as f:
            for url in progbar(urls, msg.OBATAIN_URLS):
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
        for url in progbar( urlLists.get_list_of_lists()[currLevel], msg.RECOLECT_IMG):
            
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
            for img in progbar(urls, "[" + str(lvl) + "] " + msg.DOWNLOAD):
                f = executor.submit(download, img)
                beforename =  img.rsplit('/', 1)[-2]
                img_name = beforename.rsplit('/', 1)[-1]
                myf.write(img_name + '\n')


if __name__ == '__main__':
	main()