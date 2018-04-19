import MySQLdb
from models import UserModel
import time
from crawl_relationships import crawl_users

class crawler():
    url = "localhost"
    username = "root"
    password = "3228932"
    dbname = "myfacebookcrawler"
    def get_connection(self):
        return MySQLdb.connect(host=self.url, user=self.username, passwd=self.password, db=self.dbname, charset="utf8")
    def start(self):
        db = self.get_connection()
        cursor = db.cursor()

        # 对表加锁
        sql = "lock tables fb_users write;"
        cursor.execute(sql)

        # 找到一条可以爬取的记录
        sql = "select * from fb_users where dbstatus = 1 limit 1"
        cursor.execute(sql)

        record = cursor.fetchone()
        if record != None:
            print(record)
            user = UserModel(id=record[0], name=record[1], username=record[2], url=record[5], profile=record[4],
                             dbstatus=record[6])
            sql = "update fb_users set dbstatus = %d where id = %d" % (2, user.id)
            print(sql)
            cursor.execute(sql)
        else:
            user = None
            print("no user to crawl")

        userlist = crawl_users(user.url)

        for user in userlist:
            user.name = user.name.replace("\"", "\\\"")
            user.username = user.username.replace("\"", "\\\"")
            user.profile = user.profile.replace("\"", "\\\"")
            user.url = user.url.replace("\"", "\\\"")
            sql = 'insert ignore into fb_users values (null, "%s", "%s", null, "%s", "%s", %d, null, null)' % (
            user.name, user.username, user.profile, user.url, user.dbstatus)
            print(sql)
            cursor.execute(sql)

        sql = "update fb_users set dbstatus = %d where id = %d" % (3, user.id)
        print(sql)
        cursor.execute(sql)
        sql = "update fb_users set craweled_time = '%s' where id = %d" % (
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), user.id)
        print(sql)
        cursor.execute(sql)
        sql = "unlock tables"
        cursor.execute(sql)

        db.commit()
        db.close()

