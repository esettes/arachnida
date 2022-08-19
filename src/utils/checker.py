from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm
import os
from alive_progress import alive_bar
import utils.misc as msg

def is_valid(url):
    """
	Checks whether `url` is a valid URL. Check netloc(domain name)
	and squeme(protocol) are there.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    """
    Returns all image URLs on a `url` array
    """
    getURL = requests.get(url)
    msg.status_msg(str(getURL.status_code))
    soup = bs(getURL.content, "lxml")
    
    urls = []
    all = soup.find_all("img")
    for img in tqdm(soup.find_all("img"), "Extracting images"):
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
            msg.info_msg(img_url)
            if is_valid(img_url):
                urls.append(img_url)
    return urls

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(pathname, url.split("/")[-1])
    f_name = filename[10:]
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {f_name}", total=file_size ,bar_format="{desc:<5}{percentage:3.0f}%|{bar}{r_bar}", colour='green', unit_scale=True, unit_divisor=1024)
    try:
        with open(filename, "wb") as f:
            for data in progress.iterable:
                f.write(data)
                progress.update(len(data))
    except:
        pass

def CheckImgExtension(f_name):
    if f_name.endswith('.gif') or f_name.endswith('.jpg') or \
        f_name.endswith('.jpeg') or f_name.endswith('.png') or \
            f_name.endswith('.bmp'):
                return True
    else:
        return False