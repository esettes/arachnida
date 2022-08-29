import requests
import utils.misc as msg

from utils.requestclass import CheckStatusCode

def download(url):#, path_):
    """
    Downloads a file given an URL and puts it in the folder `pathname`

    ** Set pathname before call executor.map progress bar **
    """
    #for url in urls:
    path_ = url.rsplit('/', 1)[-1] # path into url, at moment only way i found to put path here
    beforename =  url.rsplit('/', 1)[-2]
    #print(msg.BLUEAQUA + beforename.rsplit('/', 1)[-1] + msg.B_END + msg.END)
    response = requests.get(beforename, timeout=3)
    img_name = beforename.rsplit('/', 1)[-1]
        #response = requests.get(url)
        #print(url)
        #img_name = url.rsplit('/', 1)[-1]
       # print(img_name)
    with open(str(path_) + '/' + img_name, 'wb') as f:
        f.write(response.content)

def download2(path_, urls):
    """
    Downloads the `urls` passed as param. and puts it in the folder `pathname`
    """
    img_name = url.rsplit('/', 1)[-1]
    for url in urls:
        response = requests.get(url)#, timeout=3)
        if CheckStatusCode(response):
            msg.STATUS_CODE(response.status_code)
        with open(str(path_) + '/' + img_name, 'wb') as f:
            f.write(response.content)

