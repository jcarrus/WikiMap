import os
import MySQLdb as mdb
import csv

def uploadPages():
    con = mdb.connect('sql.mit.edu', 'jcarrus', 'ver17map',
                      'jcarrus+WikiMap')
    cur = con.cursor()
    index = 0
    data = []
    cur.execute("TRUNCATE TABLE ids")
    try:
        with open('WikiMapAll', 'r') as file:
            csvreader = csv.reader(file)
            for i in csvreader:
                data.append( (int(i[0]), i[1]) )
                index += 1
                if index % 10000 == 0:
                    cur.executemany("INSERT IGNORE INTO ids (curid, title) VALUES (%s, %s);", data)
                    print index
                    data = []
            cur.executemany("INSERT IGNORE INTO ids (curid, title) VALUES (%s, %s);", data)
            print index
    except Exception as e:
        print e
    cur.close()
            
            
uploadPages()
