#!/usr/bin/python3.9
from genericpath import isdir
from importlib.resources import path
from os.path import split, splitext
import sys
import warnings
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PIL.ExifTags import TAGS
from utils.misc import CUSTOM_TAGS
from utils.scorpionclass import ScorpionProperties
from utils.scorpionutils import SetScorpionArgs, getMetadata
import utils.misc as msg
from datetime import date
from datetime import datetime as dt
import pytz

imgExtension = {
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.bmp'
}

def main(argv):

    args = SetScorpionArgs()
    scorpion = ScorpionProperties()
    images = []

    madrid = pytz.timezone("Europe/Madrid")
    datename = date.today()
    now = dt.now(madrid)
    s = now.strftime("%I:%M:%S")

    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
    if args.path != 'data':
        scorpion.set_path(args.path)
    if args.logpath != 'log_images':
        scorpion.set_logpath(args.logpath)
    images = scorpion.get_source(scorpion.get_path())

    pathname_ = str(scorpion.get_logpath()) + '/' + datename.isoformat() + '_' + s + '.txt'

    if isdir(pathname_):
        with open(pathname_, 'a') as f:
            for img in images:
                imgSplit = split(img)
                ext = splitext(imgSplit[1])
                if ext[1] in imgExtension:
                    f.write('\n\n* * * [ ' + img +  ' ] * * * \n')
                    getMetadata(f, img)
                    try:
                        image = Image.open(img)
                    except Exception:
                        continue
                    exifdata = image.getexif()
                    for tagid in exifdata:
                        tagname = TAGS.get(tagid, tagid)
                        value = exifdata.get(tagid)
                        try:
                            f.write(str(tagname[:25]) + ':' + str(value) + '\n')
                        except Exception:
                            pass
    else:
        return
    return

if __name__ == '__main__':
	main(sys.argv)