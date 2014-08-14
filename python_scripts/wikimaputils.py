import os
import datetime
from Queue import Queue
from threading import Thread

class Record:
    
    def __init__(self, directory, numLines, max_queue_size = 400):
        self.directory = directory
        self.numLines = numLines
        self.now = str(datetime.datetime.now())

        self.q = Queue(max_queue_size)
        self.t = Thread(target = writeQueue, args = (self.now, self.directory, self.q, self.numLines))
        self.t.daemon = True
        self.t.start()

    def writeline(self, line):
        self.q.put(line, True)

    def close(self):
        self.q.put(False, True)

def writeQueue(starttime, directory, q, numLines):
    path = "/mnt/data"
    if not os.path.exists('%s/%s/%s/' % (path, directory, starttime)):
        os.makedirs('%s/%s/%s/' % (path, directory, starttime))
    filenum = 1
    f = open('%s/%s/%s/%05d' % (path, directory, starttime, filenum), 'w')
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
                f = open('%s/%s/%s/%05d' % (path, directory, starttime, filenum), 'w')
            q.task_done()
        except:
            print "write error on line: %s" % line
            raise
