import requests

def download(url):
    """
    Downloads a file given an URL and puts it in the folder `pathname`

    ** Set pathname before call executor.map progress bar **
    """
    path_ = url.rsplit('ñ', 1)[-1]
    beforename =  url.rsplit('ñ', 1)[-2]
    try:
        response = requests.get(beforename, timeout=3)
        img_name = beforename.rsplit('/', 1)[-1]
        with open(str(path_) + '/' + img_name, 'wb') as f:
            f.write(response.content)
    except Exception:
        pass

