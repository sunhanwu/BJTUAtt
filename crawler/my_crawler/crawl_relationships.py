from selenium import webdriver
import time
from DBHelper import DBHelper
from models import UserModel, RelationshipModel
import json
import logging
import os
import threading
logger = logging.getLogger()
logger_name = ""

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
    try:
        cookies = [{'domain': '.facebook.com', 'httpOnly': False, 'name': '_js_reg_fb_ref', 'path': '/', 'secure': True, 'value': 'https%3A%2F%2Fwww.facebook.com%2Flogin.php'}, {'domain': '.facebook.com', 'expiry': 1516001667, 'httpOnly': False, 'name': 'wd', 'path': '/', 'secure': True, 'value': '1036x675'}, {'domain': '.facebook.com', 'expiry': 1578468860.767658, 'httpOnly': True, 'name': 'datr', 'path': '/', 'secure': True, 'value': '9x5TWjf--2UlNXPTlCzQJQav'}, {'domain': '.facebook.com', 'expiry': 1523172865.671106, 'httpOnly': True, 'name': 'xs', 'path': '/', 'secure': True, 'value': '42%3ASmJNEiGSJJuUcw%3A2%3A1515396864%3A-1%3A-1'}, {'domain': '.facebook.com', 'expiry': 1523172865.671058, 'httpOnly': False, 'name': 'c_user', 'path': '/', 'secure': True, 'value': '100023787982804'}, {'domain': '.facebook.com', 'expiry': 2146116886, 'httpOnly': False, 'name': 'presence', 'path': '/', 'secure': True, 'value': 'EDvF3EtimeF1515396868EuserFA21B23787982804A2EstateFDutF1515396868474CEchF_7bCC'}, {'domain': '.facebook.com', 'httpOnly': True, 'name': 'reg_fb_gate', 'path': '/', 'secure': True, 'value': 'https%3A%2F%2Fwww.facebook.com%2Flogin.php'}, {'domain': '.facebook.com', 'httpOnly': True, 'name': 'reg_fb_ref', 'path': '/', 'secure': True, 'value': 'https%3A%2F%2Fwww.facebook.com%2Flogin.php'}, {'domain': '.facebook.com', 'expiry': 1523172865.671221, 'httpOnly': True, 'name': 'pl', 'path': '/', 'secure': True, 'value': 'n'}, {'domain': '.facebook.com', 'expiry': 1523172865.671157, 'httpOnly': True, 'name': 'fr', 'path': '/', 'secure': True, 'value': '0gmmAyWFWKwz8NDDm.AWWNMwPj6uIlDfBEpygG-23q9aI.BaUx73.ig.AAA.0.0.BaUx8A.AWWG8n7b'}, {'domain': '.facebook.com', 'expiry': 1516001664, 'httpOnly': False, 'name': 'dpr', 'path': '/', 'secure': True, 'value': '1.25'}, {'domain': '.facebook.com', 'expiry': 1578468865.670949, 'httpOnly': True, 'name': 'sb', 'path': '/', 'secure': True, 'value': 'AB9TWrVWFQf-rE7oHCqWM2bb'}]

        driver.get("https://www.facebook.com/login.php")
        for cookie in cookies:
            driver.add_cookie(cookie)
        #print(driver.get_cookies())
        #driver.get("https://www.facebook.com/juliancha.julian")

        rt = get_relationships(driver, user)
        rt_data["friends"] = rt["friends"]
        rt_data["fb_id"] = rt["fb_id"]
    except Exception as e:
        print(e)
    #get_about(driver, user)
    except KeyboardInterrupt as e:
        raise e
    finally:
        driver.close()
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
        if cnt % 10 == 0:
            if now == last:
                break
            last = now
        cnt = cnt + 1

    # driver.execute_script(script)
    blocks = driver.find_elements_by_xpath('//div[@data-testid="friend_list_item"]/div/div[2]/div')
    # print("%d friends in total " % len(blocks))
    # print("%d friends in total " % len(blocks))
    logger.info("%d friends in total " % len(blocks))
    friend_list = []

    if len(blocks):
        for block in blocks:
            atag = block.find_elements_by_tag_name("a")[0]
            name = atag.text
            # print("name : %s" % (name))
            url = atag.get_attribute("href")
            if "profile.php" in url:
                url = url[0:url.find("&")]
            elif url.find("?") != -1:
                url = url[0:url.find("?")]
            # print("url : %s" % (url))
            username = url[url.rfind("/") + 1:]
            # print("username : %s" % (username))
            profile = block.find_elements_by_tag_name("ul")
            if len(profile):
                profile = profile[0].text
            else:
                profile = ""
            # print("profile : %s" % (profile))
            friend = UserModel(name=name, username=username, url=url, profile=profile)
            friend_list.append(friend)
            # print("*" * 64)
    return {"friends": friend_list, "fb_id": fb_id}


def get_about(driver, user):
    # prefix = user.url + "/about?lst=100022121971043%3A100023449741881%3A1515745479&pnref=about&section="
    # sections = ["education",
    #              "living",
    #             "contact-info",
    #             "relationship",
    #              ]
    # for section in sections:
    #     driver.get(prefix + section)
    #     time.sleep(2)
    driver.get(user.url + "/about")

    driver.find_element_by_xpath("//a[@data-testid='nav_edu_work']").click()
    time.sleep(2)

    driver.find_element_by_xpath("//a[@data-testid='nav_places']").click()
    time.sleep(2)

    driver.find_element_by_xpath("//a[@data-testid='nav_contact_basic']").click()
    time.sleep(2)

    driver.find_element_by_xpath("//a[@data-testid='nav_all_relationships']").click()
    time.sleep(2)

    driver.find_element_by_xpath("//a[@data-testid='nav_about']").click()
    time.sleep(2)

    driver.find_element_by_xpath("//a[@data-testid='nav_year_overviews']").click()
    time.sleep(2)


def init():
    user = UserModel(name="Selina Joey", username="selina.joey", url="https://www.facebook.com/selina.joey",
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
                time.sleep(1)
        #print(user.url)
        logger.info("to crawl user %s" % user.username)
   
        result = crawl_users(user)
        user_list = result["friends"]
        dbhelper.save_friends(user, user_list)

        user.friend_num = len(user_list)
        user.fb_id = result["fb_id"]
        dbhelper.crawled_over(user)
    except Exception as e:
        logger.error(e)
        logger.error("Oops! Something wrong! ")
        if user != None:
            dbhelper.crawl_failed(user)
    except KeyboardInterrupt as e:
        logger.error(e)
        logger.error("Interrupted!! ")
        if user != None:
            dbhelper.crawl_interrupted(user)
        exit(0)


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
                     url="https://www.facebook.com/profile.php?id=100004603682769", profile="你好")
    crawl_users(user)
