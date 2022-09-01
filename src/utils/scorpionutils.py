import sys
import utils.misc as msg
import argparse
from pathlib import Path

def SetScorpionArgs():
    head = """  """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=head)
    parser.add_argument('-a','--all', action='store_true', help="Use all pillow tags instead the few most common.")
    parser.add_argument('-p','--path', type=Path, metavar='PATH', default='data', help="Change the default path where images will be loaded. Default is /data")
    parser.add_argument('-l','--logpath', type=Path, metavar='PATH', default='log_images', help="Change the default path where the exif info will be saved. Default is /log_images")
    args = parser.parse_args()
    return args