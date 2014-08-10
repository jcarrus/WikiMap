import requests
import urllib
import urlparse
import re
import os
import traceback
import sys
import csv

def getAllBacklinks():
    if not os.path.exists('../data/backlinks/'):
        os.makedirs('../data/backlinks/')
    counter = 0
    filenum = 1
    continue_string = ''
    r = ''
    links = csv.reader(open('WikiMapAll', 'rb'))
    for i in [["1756571"]]:#, for i in links:
        print i[0]
        try:
            continue_string = ''
            while True:
                (continue_string, r) = getAllBacklinksHelper(i[0], continue_string, r)
                if continue_string == "000000":
                    f = open('../data/backlinks/lastErr', 'w')
                    f.write(r.encode('utf8'))
                    f.close()
                    print "Err"
                    break
                if continue_string == None:
                    f = open('../data/backlinks/%04d' % filenum, 'w')
                    f.write(r.encode('utf8'))
                    f.close()
                    break
                counter += 1
                if counter == 100:
                    sys.stdout.write('|')
                    f = open('../data/backlinks/%04d' % filenum, 'w')
                    f.write(r.encode('utf8'))
                    f.close()
                    r = ''
                    counter = 0
        except Exception as e:
            print traceback.format_exc()
            print e
            print 'Error on %s' %str(i)
    return "Finished"
    
def getAllBacklinksHelper(page_id, mycontinue, results):
    result = requests.get(getQuery(page_id, mycontinue)).json()
    if result == []:
        print getQuery(page_id, mycontinue)
        return ("000000", result)
    try:
        for i in result['query']['backlinks']:
            results += page_id + ',' + str(i['pageid']) + '\n'
    except:
        print result
        raise
    if 'query-continue' not in result:
        return (None, results)
    else:
        return (result['query-continue']['backlinks']['blcontinue'], results)

def getQuery(page_id, mycontinue = "", list = "backlinks", num_results = 500):
    mystr = 'http://en.wikipedia.org/w/api.php?' \
        + 'format=json' \
        + '&action=query' \
        + '&list=' + list \
        + '&bllimit=' + str(num_results) \
        + '&blpageid=' + str(page_id) \
        + '&blfilterredir=nonredirects'
    if mycontinue != "":
        mystr += '&blcontinue=' + url_fix(mycontinue)
    return mystr

def url_fix(s):
    return s.replace("&", "%26")
#print getQuery("1756571", "0|106_&_Park|30496533")
getAllBacklinks()


