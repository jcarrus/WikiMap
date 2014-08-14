import requests
import csv
from threading import Thread
from wikimaputils import Record
from Queue import Queue

def getAllBacklinks():
    numThreads = 25
    writer = Record('backlinks', 10000)
    errors = Record('errors', 10000)
    linksQueue = Queue(numThreads * 2)

    # Make a bunch of threads
    for i in range(numThreads):
        t = Thread(target = backlinksWorker, args = (linksQueue, writer, errors))
        t.daemon = True
        t.start()

    # Read from the csv and add each link to the queue
    links = csv.reader(open('WikiMapAll', 'rb'))
    for i, link in enumerate(links):
        linksQueue.put(link[0], True)
        if (i % 10000 == 0):
            print link[1]

    # Wait for the queue to finish
    linksQueue.join()

    # Close the files
    writer.close()
    errors.close()


def backlinksWorker(q, r, e):
    while True:
        try:
            # Pull from the queue
            frontlink = q.get(True)
            # Get all backlinks
            links = getBacklinksForId(frontlink)
            # Write to the file
            s = str(frontlink)
            for link in links:
                s += ',' + str(link)
            r.writeline(s)
            # Report finished
            q.task_done()
        except:
            e.writeline(str(frontlink))
            raise
            
def getBacklinksForId(page_id, blcontinue = ''):
    results = []
    # Query the database
    result = requests.get(getQuery(page_id, blcontinue)).json()
    # Add all of the backlinks to the results
    for i in result['query']['backlinks']:
        results.append(i['pageid'])
    # If there are no more, return, else, repeat.
    if 'query-continue' not in result:
        return results
    return results + getBacklinksForId(page_id, result['query-continue']['backlinks']['blcontinue'])

# Creates the apropriate Wikipedia query for given parameters
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

# Removes undesired characters from the created query url
def url_fix(url):
    return url.replace("&", "%26")

getAllBacklinks()
