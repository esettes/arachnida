#!/usr/bin/python3
from locale import currency
import time
from utils.utils import SetArgs
from utils.requestclass import Spider, get_all_images_new
from utils.listsurlclass import URLlists, get_base_images, obtain_all_href, obtain_base_href
import utils.misc as msg
#import ipdb
#ipdb.set_trace()
#ipdb.set_trace(context=6)

def	main():
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
        print(f'{msg.INFO} pathname: {spider.get_pathname()}')
    if args.recursive and args.level == 0:
        spider.set_url(args.recursive)
    if args.recursive and args.level != 0:
        spider.set_url(args.recursive)
        print(f'url: {spider.get_url()}')
        spider.set_level(args.level)

    urlLists.append_new_list()
    for i in urlLists.get_list_of_lists():
        print(i)
    urls = obtain_base_href(spider.get_url())
    print(f'spider url: {spider.get_url()}')
    urlLists.set_level_list(urls, 1)

    urlLists.append_new_img_list()
    imgs = get_base_images(spider.get_pathname(), spider.get_url())
    urlLists.set_level_list_images(imgs, 1)
    if currLevel < spider.get_level():
        currLevel += 1
        recursive_obtain_urls(currLevel, urlLists, spider, urls, imgs)
    
    with open('log/log_hrefs_list_0', 'w') as f:
        for h in urlLists.get_list_of_lists():
            for item in h:
                f.write(item)
                f.write('\n')
    
    with open('log/log_images_list_0', 'w') as f:
        for h in urlLists.get_lists_of_images():
            for item in h:
                f.write(item)
                f.write('\n')



def recursive_obtain_urls(currLevel, urlLists, spider, urls, imgs):
    while currLevel <= spider.get_level():
        u = []
        urlLists.append_new_list()
        u = obtain_all_href(urls)
        print(f'{msg.INFO} recursive urls: {u}')
        urlLists.set_level_list(u, currLevel)
        urls.clear()

        im = []
        urlLists.append_new_img_list()
        im = get_all_images_new(spider.get_pathname(), imgs)
        urlLists.set_level_list_images(im, currLevel)
        imgs.clear()

        currLevel += 1
        recursive_obtain_urls(currLevel, urlLists, spider, u, im)
    return

if __name__ == '__main__':
	main()