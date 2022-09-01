#!/usr/bin/python3.9
import sys
import time
import requests
import warnings
from utils.spiderutils import SetArgs, recursive_obtain_imgs, recursive_obtain_urls, thread_submit
from utils.spiderclass import FormatUrl, Spider, get_all_images_new, CheckBaseurl
from utils.listsurlclass import URLlists, obtain_all_href
import utils.misc as msg

def	main(argv):
    start_time = time.time()
    args = SetArgs()
    spider = Spider()
    currLevel = 0
    urlLists = URLlists()
    recursiveSearch = False


    if args.path != 'data':
        spider.set_pathname(args.path)
    if args.level != 0:
        spider.set_level(args.level)
    if args.recursive: # and args.level == 0:
        spider.set_url(args.recursive)
        recursiveSearch = True

    if args.recursive == None and args.level == 0:
        spider.set_url(argv[1])
    if args.recursive == None and args.level != 0:
        msg.err_msg("Non recursive search didn't allow level")
        return
    if args.recursive == None and args.path != 'data':
        try:
            if CheckBaseurl(argv[1]):
                spider.set_url(argv[1])
            else:
                print("URL must be the first parameter ( ./spider www.mywebpage.com -p myfolder/ )")
                return
        except Exception:
            return
    #if args.recursive: #and args.level != 0:
        #spider.set_url(args.recursive)
        #spider.set_level(args.level)


    if CheckBaseurl(spider.get_url()) == False:
        return

    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
    spider.set_base_url(spider.get_url())
    main_url = spider.get_main_url()

    url = spider.get_url()

    spider.set_base_url(FormatUrl(url, ))
    #if spider.get_url() != 

    urls = []
    urlLists.append_new_list()
    obtain_all_href(spider.get_url(), urls)
    urlLists.set_level_list(urls, 0)

    imgs = []
    urlLists.append_new_img_list()
    get_all_images_new(spider.get_pathname(), spider.get_url(), imgs, main_url)
    urlLists.set_level_list_images(imgs, 0, main_url)

    if recursiveSearch:
        if currLevel < spider.get_level():
            thread_submit(imgs, currLevel)
            currLevel += 1
            nxtLevel = currLevel
            recursive_obtain_urls(nxtLevel, urlLists, spider, urls)
            time.sleep(0.5)
            recursive_obtain_imgs(currLevel, urlLists, spider, imgs, main_url)
        #elif currLevel == spider.get_level():
        #    thread_submit(imgs, currLevel)
    thread_submit(imgs, currLevel)


    time.sleep(0.5)
    print(msg.DONE)
    print("--- %s seconds ---" % (time.time() - start_time))
    return


if __name__ == '__main__':
	main(sys.argv)