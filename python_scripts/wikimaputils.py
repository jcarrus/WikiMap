import os
import datetime
from Queue import Queue
from threading import Thread

class Record:

    def __init__(self, directory, numLines):
        self.directory = directory
        self.numLines = numLines
        self.now = str(datetime.datetime.now())

        self.q = Queue(max_queue_size)
        self.t = Thread(target = writeQueue, args = (self.directory, self.now, self.filenum, q, self.numlines))
        self.t.daemon = true
        self.t.start()


    # Need to figure out how to stop this properly. I could have the close method just
    # send a line that would tell the queue to close. But that seems a bit messy.
    def writeQueue(starttime, directory, q, numlines):
        if not os.path.exists('../data/%s/%s/' % (directory, starttime)):
            os.makedirs('../data/%s/%s/' % (directory, starttime))
        filenum = 1
        f = open('../data/%s/%s/%05d' % (directory, starttime, filenum), 'w')
        currentLines = 0
        while True:
            line = q.get(True)
            try:
                f.write(line + '\n')
                currentLines += 1
                if (currentLines % numLines == 0):
                    f.close()
                    currentLines = 0
                    filenum += 1
                    f = open('../data/%s/%s/%05d' % (directory, now, filenum), 'w')
            except:
                print "write error on line: %s" % line

    def writeline(self, line):
        self.q.put(line, True)
    def close(self):
        self.f.close()
