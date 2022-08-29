from time import sleep
from multiprocessing import Process
from multiprocessing import Value
 
# custom process class
class ImagesProcess(Process):
    # override the constructor
    def __init__(self, currLevel, urlLists, spider, imgs):
        # execute the base constructor
        Process.__init__(self)
        # initialize integer attribute
        self.data = Value('i', 0)
 
    # override the run function
    def run(self):
        # block for a moment
        sleep(1)
        # store the data variable
        self.data.value = 99
        # report stored value
        print(f'Child stored: {self.data.value}')
 
# entry point
if __name__ == '__main__':
    # create the process
    process = ImagesProcess()
    # start the process
    process.start()
    # wait for the process to finish
    print('Waiting for the child process to finish')
    # block until child process is terminated
    process.join()
    # report the process attribute
    print(f'Parent got: {process.data.value}')