import os
import csv
import datetime


def splitLinks():
    now = str(datetime.datetime.now())
    if not os.path.exists('../data/splitlinks/%s/' % now):
        os.makedirs('../data/splitlinks/%s/' % now)
    filenum = 1
    data = ''
    size = 10000
    links = csv.reader(open('WikiMapAll', 'rb'))
    for i, link in enumerate(links):
        data += link[0] + ',' + link[1] + '\n'
        if (i % size == 0 and i > 0):
            f = open('../data/splitlinks/%s/%04d' % (now, filenum), 'w')
            f.write(data)
            f.close()
            filenum += 1
            data = ""


splitLinks()
