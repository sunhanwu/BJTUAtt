from crawl_relationships import multi_run_re_crawler, init
from multiprocessing import Process, Pool
import threading
from DBHelper import DBHelper
import sys

if __name__ == "__main__":

    num = int(sys.argv[1])
    procs = []
    dbhelper = DBHelper
    init()
    # for i in range(0, num):
    #     procs.append(Process(target=multi_run_re_crawler))
    # for p in procs:
    #     p.start()
    #     p.join()
    threads = []
    for i in range(0, num):
        t = threading.Thread(target=multi_run_re_crawler)
        t.setName("t%d" % i)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()

