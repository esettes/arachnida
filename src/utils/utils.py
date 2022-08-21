import sys
import utils.misc as msg
import argparse
from pathlib import Path
from argparse import RawTextHelpFormatter

def progressbar(it, prefix="", size=60, out=sys.stdout): # Python3.3+
    """
    Custom progress bar.
     Arguments:
        `it` Number of items
         `prefix` Informative message near bar
        `size` The size of th bar
         `out` Output 
    """
    count = len(it)
    try:
        def show(j):
            x = int(size*j/count)
            print("{}[{}{}] {}/{}".format(prefix, msg.LOAD*x, msg.DOT*(size-x), j, count), # █
                   end='\r', file=out, flush=True)
    except Exception:
        pass
    show(0)
    try:
        for i, item in enumerate(it):
            yield item
            show(i+1)
    except Exception:
        pass
    print( flush=True, file=out)


def SetArgs():
    head = """  """
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description=head)
    group = parser.add_argument_group('Required argument')
    group.add_argument('-r','--recursive', type=str, metavar='URL', nargs='?', default=None, help="Download recursively images from passed URL.")
    parser.add_argument('-l','--level', type=int, metavar='LEVEL', nargs='?', const=5, default=0, choices=range(0,16), help="Depth level to \
download images from web, if not indicate flag, default is 0. \
If indicate flag but not set a value for it, the default val is 5")

    #excludeGroup = parser.add_mutually_exclusive_group()
    parser.add_argument('-p','--path', type=Path, metavar='PATH', default='data', help="Change the default path to store downloaded images. Thefault path is /data")
    args = parser.parse_args()
    return args




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