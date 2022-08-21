from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs
import requests
import os
import utils.misc as msg
from utils.progressbar import progressbar as progbar

def is_valid(url):
    """
	Checks whether `url` is a valid URL. Check netloc(domain name)
	and squeme(protocol) are there.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    """
    Obtains all valid images(jpg, jpeg, gif, bmp) URLs.

    Return:
        `urls` list
    """
    getURL = requests.get(url)
    msg.status_msg(str(getURL.status_code))
    soup = bs(getURL.content, "lxml")
    urls = []
    all = soup.find_all("img")
   
    for img in progbar(all, msg.RECOLECT_IMG):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        # if url have key-value, remove all after '?'
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if CheckImgExtension(img_url):
            if not img_url in urls:
                if is_valid(img_url):
                    urls.append(img_url)
    msg.info_msg('Removed ' + str(len(all) - len(urls)) + ' images.')
    return urls

def get_level_urls(url):
    """
    Extracts the current level hrefs

    Return:
        `hrefs` list
    """
    getURL = requests.get(url)
    msg.status_msg(str(getURL.status_code))
    soup = bs(getURL.content, "lxml")
    hrefs = []
    all = soup.find_all('a')

    for h in progbar(all, msg.RECOLECT_HREF):
        obtain = h.get('href')
        if not obtain in hrefs:
            hrefs.append(obtain)
    msg.info_msg('Removed ' + str(len(all) - len(hrefs)) + ' hrefs.')
    return hrefs

def download(url):
    """
    Downloads a file given an URL and puts it in the folder `pathname`

    ** Set pathname before call executor.map progress bar **
    """
    pathname = "img_folder2"
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    response = requests.get(url)
    img_name = url.rsplit('/', 1)[-1]
    with open(pathname + '/' + img_name, 'wb') as f:
        f.write(response.content)


def CheckImgExtension(f_name):
    if f_name.endswith('.gif') or f_name.endswith('.jpg') or \
        f_name.endswith('.jpeg') or f_name.endswith('.png') or \
            f_name.endswith('.bmp'):
                return True
    else:
        return False
