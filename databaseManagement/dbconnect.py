import os
import MySQLdb as mdb
import csv

def loadCSV():
    con = mdb.connect('sql.mit.edu', 'jcarrus', 'ver17map',
                      'jcarrus+WikiMap')
    cur = con.cursor()
    index = 0
    cur.execute("TRUNCATE TABLE ids")
    with open('WikiMapAll', 'rb') as file:
        csvreader = csv.reader(file)
        for i in csvreader:
            index += 1
            cur.execute("""
            INSERT INTO ids
            (curid, title)
            VALUES (%s, %s);
            """, (i[0],i[1]))
            if index % 100 == 0:
                print index


loadCSV()
