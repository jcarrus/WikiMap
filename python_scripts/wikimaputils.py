import os
import datetime

class Record:

    def __init__(self, directory, numLines):
        self.directory = directory
        self.numLines = numLines
        self.now = str(datetime.datetime.now())
        self.currentLines = 0
        self.filenum = 1

        if not os.path.exists('../data/%s/%s/' % (self.directory, self.now)):
            os.makedirs('../data/%s/%s/' % (self.directory, self.now))

        self.f = open('../data/%s/%s/%05d' % (self.directory, self.now, self.filenum), 'w')
        

    def writeline(self, line):
        self.f.write(line + '\n')
        self.currentLines += 1
        if (self.currentLines % self.numLines == 0):
            self.f.close()
            self.currentLines = 0
            self.filenum += 1
            self.f = open('../data/%s/%s/%05d' % (self.directory, self.now, self.filenum), 'w')
    
    def close(self):
        self.f.close()
