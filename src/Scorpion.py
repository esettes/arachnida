#!/usr/bin/python3.9
import sys
import warnings
from PIL import Image
from PIL.ExifTags import TAGS
from utils.misc import CUSTOM_TAGS
from utils.scorpionproperties import ScorpionProperties
from utils.scorpionutils import SetScorpionArgs
import utils.misc as msg

def main(argv):

    args = SetScorpionArgs()
    scorpion = ScorpionProperties()
    tags = TAGS
    images = []

    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')
    if args.path != 'data':
        scorpion.set_path(args.path)
    if args.logpath != 'log_images':
        scorpion.set_logpath(args.logpath)
    if args.all:
        tags = CUSTOM_TAGS
    images = scorpion.get_source(scorpion.get_path())



    for img in images:
        print(f'{msg.INFO} {img}')
        image = Image.open(img)
        exifdata = image.getexif()
        for tagid in exifdata:
            # getting the tag name instead of tag id
            tagname = tags.get(tagid, tagid)
            # passing the tagid to get its respective value
            value = exifdata.get(tagid)
            # printing the final result
            print(f"{tagname:25}: {value}")
    return

if __name__ == '__main__':
	main(sys.argv)