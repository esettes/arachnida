from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs
import requests
from tqdm import tqdm
import os
from alive_progress import alive_bar
from alive_progress import alive_it


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
    soup = bs(requests.get(url).content, "lxml")
    urls = []
    all = soup.find_all("img")
    with alive_bar(len(all)) as bar:
        for img in all:
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
                if is_valid(img_url):
                    urls.append(img_url)
                bar()
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
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    bar = alive_it(response.iter_content(1024), finalize=lambda bar: bar.text('Success!'))
    try:
        with open(filename, "wb") as f:
            for data in bar:
                # write data read to the file
                f.write(data)
                # update the progress bar manually
                progress.update(len(data))
    except:
        pass