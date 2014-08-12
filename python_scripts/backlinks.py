import requests
import csv
from wikimaputils import Record

def getAllBacklinks():
    writer = Record('backlinks', 10000)
    links = csv.reader(open('WikiMapAll', 'rb'))
    errors = Record('errors', 10000)
    for link in links:
        try:
            backlinks = getBacklinksForId(link[0])
            for backlink in backlinks:
                writer.writeline(str(link[0]) + ',' + str(backlink))
        except:
            errors.writeline(str(link))
    writer.close()
    errors.close()

def getBacklinksForId(page_id, blcontinue = ''):
    results = []
    result = requests.get(getQuery(page_id, blcontinue)).json()
    for i in result['query']['backlinks']:
        results.append(i['pageid'])
    if 'query-continue' not in result:
        return results
    return results + getBacklinksForId(page_id, result['query-continue']['backlinks']['blcontinue'])

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

getAllBacklinks()
