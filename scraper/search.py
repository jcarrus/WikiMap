import requests
import urllib
import urlparse
import re


# The query for hitler as a research example: http://en.wikipedia.org/w/api.php?action=query&list=backlinks&bltitle=Adolf_Hitler&bllimit=500&blfilterredir=nonredirects&blcontinue=0|Adolf_Hitler|51534&continue=

def search(start, results):
    if len(start) == 0:
        myfrom = ""
    else:
        myfrom = "&gapfrom=" + url_fix(start)
    result = requests.get("http://en.wikipedia.org/w/api.php?format=json&action=query&generator=allpages&gaplimit=500" + myfrom).json()
    for i in result['query']['pages']:
        results += i + ","
    if "query-continue" not in result:
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
    return re.sub("&", "%26", mys)

def main():
    counter = 0
    filenum = 1
    s = ""
    r = ""
    while True:
        (s, r) = search(s, r)
        if s == None:
            f = open("%04d" % filenum, 'a')
            f.write(r)
            f.close()
            break
        counter += 1
        if counter == 1:
            f = open("%04d" % filenum, 'a')
            f.write(r)
            f.close()
            r = ""
            counter = 0
            filenum += 1
    print "Finished"

main()
