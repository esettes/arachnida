import utils.misc as msg
import argparse
from pathlib import Path
from PIL import Image
from os.path import getsize

def SetScorpionArgs():
    head = """  """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=head)
    parser.add_argument('-p','--path', type=Path, metavar='PATH', default='data', help="Change the default path where images will be loaded. Default is /data")
    parser.add_argument('-l','--logpath', type=Path, metavar='PATH', default='log_images', help="Change the default path where the exif info will be saved. Default is /log_images")
    args = parser.parse_args()
    return args

def getMetadata(f, imagepath):
    try:
        image = Image.open(imagepath)
        format = image.format
        description = image.format_description
        height = image.height
        width = image.width
        mode = image.mode
        size = round((getsize(imagepath) / 1024), 1)
        animate = getattr(image, "is_animated", False)
        frames = getattr(image, "n_frames", 1)
        f.write(f'Format: {format} \n')
        f.write(f'Description: {description}\n')
        f.write(f'Height: {height}\n')
        f.write(f'Width: {width}\n')
        f.write(f'Mode: {mode}\n')
        f.write(f'Size: {size}\n')
        f.write(f'Animate: {animate}\n')
        f.write(f'Frames: {frames}\n')


    except:
        msg.err_msg('Invalid image path.')