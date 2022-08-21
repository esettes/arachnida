from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup as bs
import requests
import os
import utils.misc as msg
from utils.utils import progressbar as progbar
from utils.requestclass import Spider

def is_valid(url):
    """
	Checks whether `url` is a valid URL. Check netloc(domain name)
	and squeme(protocol) are there.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def download(url):
    """
    Downloads a file given an URL and puts it in the folder `pathname`

    ** Set pathname before call executor.map progress bar **
    """
    path_ = url.rsplit('/', 1)[-1] # path into url, at moment only way i found to put path here
    beforename =  url.rsplit('/', 1)[-2]
    #print(msg.BLUEAQUA + beforename.rsplit('/', 1)[-1] + msg.B_END + msg.END)
    response = requests.get(beforename)
    img_name = beforename.rsplit('/', 1)[-1]
    with open(path_ + '/' + img_name, 'wb') as f:
        f.write(response.content)

