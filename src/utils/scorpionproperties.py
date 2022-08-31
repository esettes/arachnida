

class ScorpionProperties:
    def __init__(self):
        self.all = False
        self.path = 'data'
        self.logpath = 'log_images'
        self.source = []

    def set_path(self, p):
        self.path = p

    def set_logpath(self, lp):
        self.logpath = lp

    def get_path(self):
        return self.path

    def get_logpath(self):
        return self.logpath

    def set_source_list(self, path):
        