import MySQLdb as mdb

def connect():
    con = mdb.connect('sql.mit.edu', 'jcarrus', 'ver17map',
                      'jcarrus+WikiMap')
    return con.cursor()
