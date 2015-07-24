import sqlite3
from contextlib import closing

def connect_db(db_name):
    return sqlite3.connect(db_name)

with closing(connect_db('dashboard.db')) as db:
    cur = db.cursor().execute('select * from myrio_roborio_2016_stack_dashboard')
    for row in cur.fetchall():
        print row
    
