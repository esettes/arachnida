from genericpath import isdir
from os import listdir
from os.path import isfile, join
import utils.misc as msg

class ScorpionProperties:
    def __init__(self):
        self.all = False
        self.path = 'data'
        self.logpath = 'log_images'
        self.source = []

    def set_path(self, p):
        self.path = p
    
    def get_path(self):
        return self.path

    def set_logpath(self, lp):
        self.logpath = lp

    def get_path(self):
        return self.path

    def get_logpath(self):
        return self.logpath
    
    def get_source(self, path):
        if isdir(path):
            for f in listdir(path):
                img = join(path, f)
                if isfile(img):
                    self.source.append(img)
            return self.source
        else:
            msg.err_msg('Invalid or non existing path.')
