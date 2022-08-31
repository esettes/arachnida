#!/usr/bin/python3.9
import sys
from PIL import Image
from PIL.ExifTags import TAGS
from utils.misc import CUSTOM_TAGS
from utils.scorpionproperties import ScorpionProperties
from utils.scorpionutils import SetScorpionArgs 

def main(argv):

    args = SetScorpionArgs()
    scorpion = ScorpionProperties()
    exifdata = image.getexif()

    if args.path != 'data':
        scorpion.set_path(args.path)
    if args.logpath != 'log_images':
        scorpion.set_logpath(args.logpath)
    if args.all:
        exifdata = CUSTOM_TAGS

    
    # open the image
    image = Image.open(argv[1])
    print("hello")
    # extracting the exif metadata
    
    # looping through all the tags present in exifdata
    for tagid in exifdata:
        
        # getting the tag name instead of tag id
        tagname = TAGS.get(tagid, tagid)
        tag2 = TAGS.get(0x010F, )
        # passing the tagid to get its respective value
        value = exifdata.get(tagid)
        
        # printing the final result
        print(f"{tagname:25}: {value}")
    return

if __name__ == '__main__':
	main(sys.argv)