import MySQLdb
from DBUtils.PooledDB import PooledDB
from models import UserModel
import logging
import os
import time
import threading

class DBHelper:
    #host = "localhost"
    host = "211.71.75.171"
    port = 3306
    username = "root"
    password = "abcd1234"
    dbname = "myfbcrawler"
    pool = PooledDB(creator=MySQLdb, mincached=3, maxcached=10, host=host, port=port, user=username,
                    passwd=password, db=dbname, use_unicode=False, charset="utf8")

    def __init__(self):
        pass

    def close(self, conn):
        conn.close()

    def save_user(self, user):

        db = self.pool.connection()
        cursor = db.cursor()

        sql = "insert ignore into fb_users values (null, %s, %s, null, %s, %s, %s)"
        values = [user.name, user.username, user.profile, user.url,
                  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))]
        cursor.execute(sql, values)
        if cursor.rowcount != 0:
            sql = "select @@identity from fb_users limit 1"
            cursor.execute(sql)
            record = cursor.fetchone()
            uid = record[0]
            user.uid = uid
            sql = "insert ignore into crawl_status values (%s, %s, null, null)"
            values = [uid, 1]
            cursor.execute(sql, values)
        db.commit()
        db.close()

        return user

    def save_friends(self, user, friendlist):
        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("saving %d users.............." % len(friendlist))
        db = self.pool.connection()
        cursor = db.cursor()

        sql = "lock tables crawl_status write, fb_users write, fb_relationships write"
        cursor.execute(sql)
        db.commit()

        for friend in friendlist:
            sql = 'insert ignore into fb_users values (null, %s, %s, null, %s, %s, %s)'
            values = [friend.name, friend.username, friend.profile, friend.url,
                      time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))]
            cursor.execute(sql, values)

            if cursor.rowcount != 0:
                sql = "select @@identity from fb_users limit 1"
                cursor.execute(sql)
                record = cursor.fetchone()
                uid = record[0]
                logger.info("@@@@@@@@@@@@@@ %s %d" % (friend.username, uid))
                friend.uid = uid
                sql = "insert ignore into crawl_status values (%s, %s, null, null)"
                values = [uid, 1]
                cursor.execute(sql, values)

                sql = "insert ignore into fb_relationships values (null, %s, %s, null)"
                values = [user.uid, uid]
                cursor.execute(sql, values)
        db.commit()

        sql = "unlock tables"
        cursor.execute(sql)
        db.commit()
        cursor.close()
        db.close()

    def save_relationships(self, relist):
        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("saving %d relationships.............." % len(relist))
        db = self.pool.connection()
        cursor = db.cursor()
        for re in  relist:
            sql = "insert ignore into fb_relationships values (null, %s, %s, null)"
            values = [re.uid1, re.uid2]
            #self.logger.info(sql)
            #print(sql, values)
            cursor.execute(sql, values)

        db.commit()
        cursor.close()
        db.close()

    def find_user_to_crawl(self):
        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("finding users to crawl ........")
        db = self.pool.connection()
        cursor = db.cursor()

        sql = "lock tables crawl_status write, fb_users write"
        cursor.execute(sql)
        db.commit()

        sql = "select fb_users.id, fb_users.uname, fb_users.uuname, fb_users.prof, fb_users.url " \
              "from fb_users inner join crawl_status on crawl_status.id = fb_users.id where crawl_status.dbstatus = 1 " \
              "order by fb_users.id asc limit 1;"
        #self.logger.info(sql)
        cursor.execute(sql)

        record = cursor.fetchone()
        if record != None:
            #self.logger.info(record)
            user = UserModel(uid=record[0], name=record[1].decode("UTF-8"), username=record[2].decode("UTF-8"),
                             url=record[4].decode("UTF-8"), profile=record[3].decode("UTF-8"))
            sql = "update crawl_status set dbstatus = %s where id = %s"
            values = [2, user.uid]
            #self.logger.info(sql)
            #print(sql, values)
            cursor.execute(sql, values)
            logger.info("find user %s to crawl......" % user.username)
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

    def crawled_over(self, user):
        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("crawling user over %s ........" % user.username)
        # print("crawling user %s over  ........" % user.username)
        db = self.pool.connection()
        cursor = db.cursor()

        sql = "update crawl_status set dbstatus = %s, crawled_time = %s, friend_num = %s where id = %s"
        values = [3, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), user.friend_num, user.uid]
        #self.logger.info(sql)
        #print(sql, values)
        cursor.execute(sql, values)

        sql = "update fb_users set fb_id = %s where id = %s"
        values = [user.fb_id, user.uid]
        cursor.execute(sql, values)

        db.commit()
        cursor.close()
        db.close()

    def crawl_failed(self, user):
        t_name = threading.current_thread().getName()
        logger = logging.getLogger("log_%s" % t_name)
        logger.info("crawling user %s failed  ........" % user.username)
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
        logger.info("crawling user interrupted %s ........" % user.username)
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



#
# user = UserModel(name="Bernadas Cristalyn", username="chriztalynbernadaz", url= "https://www.facebook.com/chriztalynbernadaz", profile="Works at EARIST\\")
# dbHelper = DBHelper()
# dbHelper.save_user(user=user)
# user = dbHelper.find_user_to_crawl()
# if user != None:
#     logging.info(user.id)
#     dbHelper.crawled_over(user)