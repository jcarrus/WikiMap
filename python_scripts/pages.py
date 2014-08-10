import requests
import urllib
import urlparse
import re
import os
import traceback
import sys

def getAllIds():
    counter = 0
    filenum = 1
    continue_string = ''
    r = u''

    prefixes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in prefixes:
        try:
            if not os.path.exists('../data/pages/' + i):
                os.makedirs('../data/pages/' + i)
            continue_string = ''
            r = u''
            filenum = 1
            counter = 0
            while True:
                (continue_string, r) = getAllIdsHelper(continue_string, r, i)
                if continue_string == "000000":
                    f = open('../data/pages/' + i + '/lastErr', 'w')
                    f.write(r.encode('utf8'))
                    f.close()
                    print "Err"
                    break
                if continue_string == None:
                    f = open('../data/pages/' + i + '/%04d' % filenum, 'w')
                    f.write(r.encode('utf8'))
                    f.close()
                    break
                counter += 1
                if counter == 100:
                    sys.stdout.write('|')
                    f = open('../data/pages/' + i + '/%04d' % filenum, 'w')
                    f.write(r.encode('utf8'))
                    f.close()
                    r = ''
                    counter = 0
                    filenum += 1
            print 'Finished with %s' %str(i)
        except Exception as e:
            print traceback.format_exc()
            print e
            print 'Error on %s' %str(i)
    return "Finished"
    

def getAllIdsHelper(mycontinue, results, prefix = ""):
    result = requests.get(getQuery("allpages", 500, prefix, mycontinue)).json()
    if result == []:
        print getQuery("allpages", 500, prefix, mycontinue)
        return ("000000", results)
    try:
        for i in result['query']['pages']:
            results += str(result['query']['pages'][i]['pageid']) + ',' + unicode(result['query']['pages'][i]['title']) + '\n'
    except:
        print result
        print url_fix(mycontinue)
        raise
    if 'query-continue' not in result:
        return (None, results)
    else:
        return (result['query-continue']['allpages']['gapcontinue'], results)



def url_fix(s, charset='utf-8'):
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    mys = urlparse.urlunsplit((scheme, netloc, path, qs, anchor))
    return re.sub('&', '%26', mys)

def getQuery(list = "allpages", num_results = 500, prefix = "", mycontinue = ""):
    return 'http://en.wikipedia.org/w/api.php?' \
        + 'format=json' \
        + '&action=query' \
        + '&generator=' + list \
        + '&gaplimit=' + str(num_results) \
        + '&gapprefix=' + prefix \
        + '&gapfilterredir=nonredirects' \
        + '&gapcontinue=' + mycontinue

getAllIds()
