import os
import datetime
from Queue import Queue
from threading import Thread
import time
class Record:
    
    def __init__(self, directory, numLines, max_queue_size = 400):
        self.directory = directory
        self.numLines = numLines
        self.now = time.time() #str(datetime.datetime.now())

        self.q = Queue(max_queue_size)
        self.t = Thread(target = writeQueue, args = (self.now, self.directory, self.q, self.numLines))
        self.t.daemon = True
        self.t.start()

    def writeline(self, line):
        self.q.put(line, True)

    def close(self):
        self.q.put(False, True)

def writeQueue(starttime, directory, q, numLines):
    if not os.path.exists('../data/%s/%s/' % (directory, starttime)):
        os.makedirs('../data/%s/%s/' % (directory, starttime))
    filenum = 1
    f = open('../data/%s/%s/%05d' % (directory, starttime, filenum), 'w')
    currentLines = 0
    while True:
        line = q.get(True)
        if line == False:
            q.join()
            f.close()
            return
        try:
            f.write(str(line) + '\n')
            currentLines += 1
            if (currentLines % numLines == 0):
                f.close()
                currentLines = 0
                filenum += 1
                print time.time() - starttime
                return
                f = open('../data/%s/%s/%05d' % (directory, now, filenum), 'w')
            q.task_done()
        except:
            print "write error on line: %s" % line
            raise
