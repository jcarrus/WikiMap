import requests
import urllib
import urlparse
import re
import os
import traceback

# The query for hitler as a research example: http://en.wikipedia.org/w/api.php?action=query&list=backlinks&bltitle=Adolf_Hitler&bllimit=500&blfilterredir=nonredirects&blcontinue=0|Adolf_Hitler|51534&continue=

def getAllIds():
    counter = 0
    filenum = 1
    continue_string = ''
    r = u''
   # prefixes = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    prefixes = ['C']
    for i in prefixes:
        try:
            if not os.path.exists('data/' + i):
                os.makedirs('data/' + i)
            continue_string = ''
            r = u''
            filenum = 1
            counter = 0
            while True:
                (continue_string, r) = getAllIdsHelper(continue_string, r, i)
                if continue_string == "000000":
                    f = open('data/' + i + '/%04d' % filenum, 'w')
                    f.write(r.encode('utf8'))
                    f.close()
                    print "Err"
                    break
                if continue_string == None:
                    f = open('data/' + i + '/%04d' % filenum, 'w')
                    f.write(r.encode('utf8'))
                    f.close()
                    break
                counter += 1
                if counter == 100:
                    f = open('data/' + i + '/%04d' % filenum, 'w')
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
    result = requests.get('http://en.wikipedia.org/w/api.php?format=json&action=query&generator=allpages&gaplimit=477&gapprefix=' + prefix + '&gapfilterredir=nonredirects&gapcontinue=' + url_fix(mycontinue)).json()
    if result == []:
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

getAllIds()
