from selenium import webdriver
import time
from DBHelper import DBHelper
from models import UserModel, RelationshipModel
import json
import logging
import random
import threading
logger = logging.getLogger()
logger_name = ""
import traceback
cookies_list = [[{'domain': '.facebook.com', 'expiry': 1517281977, 'httpOnly': False, 'name': 'wd', 'path': '/', 'secure': True, 'value': '1036x715'}, {'domain': '.facebook.com', 'expiry': 1524453149.370761, 'httpOnly': True, 'name': 'pl', 'path': '/', 'secure': True, 'value': 'n'}, {'domain': '.facebook.com', 'expiry': 1524453149.370716, 'httpOnly': True, 'name': 'fr', 'path': '/', 'secure': True, 'value': '09rirN9CuclhJc0x8.AWUI64G7vM-SoP3ue3ery0Bjfd8.BaZqgU.5B.AAA.0.0.BaZqgd.AWWF96BH'}, {'domain': '.facebook.com', 'expiry': 1517281959, 'httpOnly': False, 'name': 'dpr', 'path': '/', 'secure': True, 'value': '1.25'}, {'domain': '.facebook.com', 'expiry': 1524453149.370665, 'httpOnly': True, 'name': 'xs', 'path': '/', 'secure': True, 'value': '31%3AcjCUs71G_fQGlg%3A2%3A1516677149%3A-1%3A-1'}, {'domain': '.facebook.com', 'expiry': 1524453149.370627, 'httpOnly': False, 'name': 'c_user', 'path': '/', 'secure': True, 'value': '100024052876713'}, {'domain': '.facebook.com', 'expiry': 1579749149.37036, 'httpOnly': True, 'name': 'datr', 'path': '/', 'secure': True, 'value': 'FKhmWgXYXc7ZE7iqdN89rl_C'}, {'domain': '.facebook.com', 'expiry': 1579749149.370586, 'httpOnly': True, 'name': 'sb', 'path': '/', 'secure': True, 'value': 'HahmWmAQmckt6fulJY57GeoF'}]
                ]

def crawl_users(user):
    rt_data = {}
    #print("crawling %s" % user.url)
    print("crawling %s" % user.url)
    logger.info("crawling %s" % user.url)
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--disable-notifications")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    #driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=chromeOptions.to_capabilities())
    try:
        cookies = random.choice(cookies_list)

        driver.get("https://www.facebook.com/login.php")
        for cookie in cookies:
            driver.add_cookie(cookie)
        #print(driver.get_cookies())
        #driver.get("https://www.facebook.com/juliancha.julian")

        rt = get_relationships(driver, user)
        rt_data["friends"] = rt["friends"]
        rt_data["fb_id"] = rt["fb_id"]
    except Exception as e:
        traceback.print_exc()
    #get_about(driver, user)
    except KeyboardInterrupt as e:
        raise e
    finally:
        driver.close()
        driver.quit()
    return rt_data


def get_relationships(driver, user):
    if "profile.php" in user.url:
        driver.get(user.url + "&sk=friends&source_ref=pb_friends_tl")
    else:
        driver.get(user.url + "/friends")
    fb_id = json.loads(driver.find_element_by_id("pagelet_timeline_main_column").get_attribute("data-gt"))[
        "profile_owner"]
    # print(fb_id)
    # driver.get("https://www.facebook.com/emygaild.santiago")
    # driver.get("https://www.facebook.com/mjmipa.aquinooooo?hc_location=friend_browser&fref=pymk")
    # print(driver.find_element_by_xpath('//a[@data-tab-key="friends"]').get_attribute("href"))
    # driver.find_element_by_xpath('//a[@data-tab-key="friends"]').click()

    # 模拟滑动
    cnt = 1
    body = driver.find_element_by_tag_name("body")
    last = body.size['height']
    while True:
        script = "window.scrollTo(0, %d);" % (body.size['height'] + 100)
        driver.execute_script(script)
        # print(script)
        time.sleep(1)
        now = body.size['height']
        # print(now)
        if cnt % 30 == 0:
            if now == last:
                break
            last = now
        cnt = cnt + 1

    # driver.execute_script(script)
    #blocks = driver.find_elements_by_xpath('//div[@data-testid="friend_list_item"]/div/div[2]/div')
    blocks = driver.find_elements_by_xpath('//ul[@data-pnref="friends"]/li/div/div')
    # print("%d friends in total " % len(blocks))
    print("%d friends in total " % len(blocks))
    #logger.info("%d friends in total " % len(blocks))
    friend_list = []

    if len(blocks):
        for block in blocks:
            atag = block.find_elements_by_tag_name("a")[0]
            name = atag.text
            #print("name : %s" % (name))
            url = atag.get_attribute("href")
            if "profile.php" in url:
                url = url[0:url.find("&")]
            elif url.find("?") != -1:
                url = url[0:url.find("?")]
            #print("url : %s" % (url))
            username = url[url.rfind("/") + 1:]
            #print("username : %s" % (username))
            profile = block.find_elements_by_tag_name("ul")
            if len(profile):
                profile = profile[0].text
            else:
                profile = ""
            #print("profile : %s" % (profile))
            friend = UserModel(name=name, username=username, url=url, profile=profile)
            friend_list.append(friend)
            #print("*" * 64)
    return {"friends": friend_list, "fb_id": fb_id}


def init():
    user = UserModel(name="Lawrence Moore", username="lawrence.moore.94", url="https://www.facebook.com/lawrence.moore.94",
                     profile="origin")
    dbhelper = DBHelper()
    dbhelper.save_user(user=user)


def run_re_crawler():
    t_name = threading.current_thread().getName()
    logger = logging.getLogger("log_%s" % t_name)
    dbhelper = DBHelper()
    user = None
    try:
        while not user:
            user = dbhelper.find_user_to_crawl()
            if not user:
                time.sleep(20)
        #print(user.url)
        logger.info("to crawl user %s" % user.username)
   
        result = crawl_users(user)
        user_list = result["friends"]
        dbhelper.save_friends(user, user_list)

        user.friend_num = len(user_list)
        user.fb_id = result["fb_id"]
        dbhelper.crawled_over(user)
    except KeyboardInterrupt as e:
        traceback.print_exc()
        logger.error(traceback.format_exc())
        logger.error("Interrupted!! ")
        if user is not None:
            dbhelper.crawl_interrupted(user)
        exit(0)
    except Exception as e:
        traceback.print_exc()
        logger.error("Oops! Something wrong! ")
        logger.error(traceback.format_exc())
        if user is not None:
            dbhelper.crawl_failed(user)


def multi_run_re_crawler():
    t_name = threading.current_thread().getName()
    print("Thread %s is running........." % t_name)
    logger = logging.getLogger("log_%s" % t_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(threadName)s %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
    fh = logging.FileHandler("logs/log_%s.log" % t_name)
    ch = logging.StreamHandler()

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    while True:
        run_re_crawler()


if __name__ == "__main__":
    # init()
    # multi_run_re_crawler("test")
    user = UserModel(name="Honey P Seraspe", username="seraspehg",
                     url="https://www.facebook.com/emangortey", profile="你好")
    userlist = crawl_users(user)["friends"]
    print(len(userlist))

