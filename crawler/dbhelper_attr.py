import MySQLdb
from DBUtils.PooledDB import PooledDB
from models import UserModel
import logging
import os
import time
import threading

class DBHelper:
    host = "localhost"
    #host = "211.71.75.171"
    port = 3306
    username = "root"
    #password = "abcd1234"
    password = "3228932"
    dbname = "myfbcrawler"
    pool = PooledDB(creator=MySQLdb, mincached=3, maxcached=10, host=host, port=port, user=username,
                    passwd=password, db=dbname, use_unicode=False, charset="utf8")

    def __init__(self):
        pass

    def close(self, conn):
        conn.close()


    def find_user_to_crawl(self):
        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("finding users to crawl ........")
        db = self.pool.connection()
        cursor = db.cursor()

        sql = "lock tables crawl_status_attr write, fb_users write"
        cursor.execute(sql)
        db.commit()

        sql = "select fb_users.id, fb_users.url  from fb_users where id = (select id from crawl_status_attr " \
              "where dbstatus = 1 order by id asc limit 1)"
        #self.logger.info(sql)
        cursor.execute(sql)

        record = cursor.fetchone()
        if record != None:
            #self.logger.info(record)
            user = UserModel(uid=record[0], name=None, username=None, url=record[1].decode("UTF-8"), profile=None)
            sql = "update crawl_status_attr set dbstatus = %s where id = %s"
            values = [2, user.uid]
            #self.logger.info(sql)
            #print(sql, values)
            cursor.execute(sql, values)
            logger.info("find user %d to crawl......" % user.uid)
        else:
            user = None
            logger.info("no user to crawl")
        db.commit()

        sql = "unlock tables"
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return user

    def save_attributes(self, user, attr_dic):
        works = attr_dic['work']
        edus = attr_dic['edu']
        skills = attr_dic['skill']
        places = attr_dic['place']
        contact = attr_dic['contact']
        basic = attr_dic['basic']
        relationship = attr_dic['relationship']
        if relationship == "":
            relationship = None
        about = attr_dic['about']
        quote = attr_dic['quote']


        birth = None
        if 'birth' in basic:
            birth = basic['birth']
        gender = None
        if 'gender' in basic:
            gender = basic['gender']
        interested_in = None
        if 'interested_in' in basic:
            interested_in = basic['interested_in']
        language = None
        if 'language' in basic:
            language = basic['language']
        religious = None
        if 'religious' in basic:
            religious = basic['religious']
        political = None
        if 'political' in basic:
            political = basic['political']

        phone = None
        if 'phone' in contact:
            phone = contact['phone']
        address = None
        if 'address' in contact:
            address = contact['address']

        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("crawling user %s over ........" % user.username)
        # print("crawling user %s over  ........" % user.username)
        db = self.pool.connection()
        cursor = db.cursor()

        sql = "replace into fb_user_attr values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = [user.uid, gender, birth, interested_in, language, religious, political, phone, address, relationship,
                  about, quote]
        cursor.execute(sql, values)

        for work in works:
            print(work)
            sql = "insert ignore into works values(null, %s)"
            values = [work]
            cursor.execute(sql, values)
            sql = "select id from works where w_name = %s"
            cursor.execute(sql, values)
            wid = cursor.fetchone()[0]
            sql = "insert ignore into user_work values(null, %s, %s)"
            values = [user.uid, wid]
            cursor.execute(sql, values)
        db.commit()
        for edu in edus:
            print(edu)
            sql = "insert ignore into education values(null, %s)"
            values = [edu]
            cursor.execute(sql, values)
            sql = "select id from education where e_name = %s"
            cursor.execute(sql, values)
            eid = cursor.fetchone()[0]
            sql = "insert ignore into user_edu values(null, %s, %s)"
            values = [user.uid, eid]
            cursor.execute(sql, values)
        db.commit()
        for place in places:
            print(place)
            sql = "insert ignore into places values(null, %s)"
            values = [place]
            cursor.execute(sql, values)

            sql = "select id from places where p_name = %s"
            cursor.execute(sql, values)

            pid = cursor.fetchone()[0]
            sql = "insert ignore into user_place values(null, %s, %s)"
            values = [user.uid, pid]
            cursor.execute(sql, values)
        db.commit()
        for skill in skills:
            print(skill)
            sql = "insert ignore into skills value(null, %s)"
            values = [skill]
            cursor.execute(sql, values)
            sql = "select id from skills where s_name = %s"
            cursor.execute(sql, values)
            sid = cursor.fetchone()[0]
            sql = "insert ignore into user_skill values(null, %s, %s)"
            values = [user.uid, sid]
            cursor.execute(sql, values)

        db.commit()
        db.close()

    def crawled_over(self, user):
        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("crawling user %s over ........" % user.uid)
        # print("crawling user %s over  ........" % user.username)
        db = self.pool.connection()
        cursor = db.cursor()

        sql = "update crawl_status_attr set dbstatus = %s, crawled_time = %s where id = %s"
        values = [3, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), user.uid]
        #self.logger.info(sql)
        #print(sql, values)
        cursor.execute(sql, values)

        db.commit()
        cursor.close()
        db.close()

    def crawl_failed(self, user):
        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("crawling user %s failed  ........" % user.uid)
        db = self.pool.connection()
        cursor = db.cursor()

        sql = "update crawl_status set dbstatus = %s where id = %s"
        values = [4, user.uid]
        #self.logger.info(sql)
        #print(sql, values)
        cursor.execute(sql, values)
        # sql = "unlock tables"
        # cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    def crawl_interrupted(self, user):
        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("crawling user interrupted %s ........" % user.uid)
        db = self.pool.connection()
        cursor = db.cursor()
        # sql = "lock tables crawl_status write"
        # self.logger.info("crawl_interrupted locking table crawl_status")
        # cursor.execute(sql)
        sql = "update crawl_status set dbstatus = %s where id = %s"
        values = [1, user.uid]
        cursor.execute(sql, values)

        # sql = "unlock tables"
        # cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    def find_all_url(self):
        db = self.pool.connection()
        cursor = db.cursor()
        sql = "select url from fb_users"
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        db.close()
        return res

    def save_status(self, uid):
        db = self.pool.connection()
        cursor = db.cursor()
        sql = "insert into crawl_status_attr values (%s, %s, null)"
        values = [uid, 1]
        cursor.execute(sql, values)
        db.commit()
        db.close()


# dbhelper = DBHelper()
#
# with open("nodes.csv", "r") as f:
#     for line in f:
#         uid = int(line.strip())
#         dbhelper.save_status(uid)
