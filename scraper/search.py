import requests
import urllib
import urlparse
import re


# The query for hitler as a research example: http://en.wikipedia.org/w/api.php?action=query&list=backlinks&bltitle=Adolf_Hitler&bllimit=500&blfilterredir=nonredirects&blcontinue=0|Adolf_Hitler|51534&continue=

def getAllIds():
    counter = 0
    filenum = 1
    s = ''
    r = u''
    while True:
        (s, r) = getAllIdsHelper(s, r)
        if s == None:
            f = open('%04d' % filenum, 'a')
            f.write(r.encode('utf8'))
            f.close()
            break
        counter += 1
        if counter == 100:
            f = open('%04d' % filenum, 'a')
            f.write(r.encode('utf8'))
            f.close()
            r = ''
            counter = 0
            filenum += 1
    return 'Finished'
    

def getAllIdsHelper(mycontinue, results):
    result = requests.get('http://en.wikipedia.org/w/api.php?action=query&list=allpages&format=json&aplimit=1&generator=allpages&gapnamespace=0&gaplimit=500&gapcontinue=' + url_fix(mycontinue)).json()
    for i in result['query']['pages']:
        results += str(result['query']['pages'][i]['pageid']) + ',' + unicode(result['query']['pages'][i]['title']) + '\n'
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
