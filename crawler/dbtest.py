import MySQLdb
from DBUtils.PooledDB import PooledDB
from models import UserModel
import logging
import os
import time
import threading
import random

class Testdb:
    #host = "localhost"
    host = "211.71.75.171"
    port = 3306
    username = "root"
    password = "abcd1234"
    #password = "3228932"
    dbname = "test"
    pool = PooledDB(creator=MySQLdb, mincached=3, maxcached=10, host=host, port=port, user=username,
                    passwd=password, db=dbname, use_unicode=False, charset="utf8")

    def __init__(self):
        pass

    def close(self, conn):
        conn.close()

    def save_test(self, testid):
        t_name = threading.current_thread().getName()
        db = self.pool.connection()
        cursor = db.cursor()
        sql = "insert into test1 values (null, %s)"
        values = [testid]
        cursor.execute(sql, values)
        time.sleep(random.randint(1, 4))
        sql = "select @@identity from test1 limit 1"
        cursor.execute(sql)
        res =cursor.fetchone()
        row_id = res[0]
        #print("%s : %d\t%d" % (t_name, row_id, testid))
        sql = "select * from test1 where id = %s"
        values = [row_id]
        cursor.execute(sql, values)
        res = cursor.fetchone()
        t_id = res[1]
        print("%s : %d\t%d\t%d" % (t_name, row_id, testid, t_id))
        if t_id != testid:
            print("%s : Oops!!!!!" % (t_name))
        db.commit()
        db.close()

def run(arg):
    testdb = Testdb()
    cnt = 1
    while True:
        num = cnt * arg
        testdb.save_test(num)
        cnt = cnt + 1

if __name__ == "__main__":
    threads = []
    for i in range(1, 10):
        t = threading.Thread(target=run, args=(i, ))
        t.setName("t%d" % i)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

