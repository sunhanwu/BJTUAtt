from selenium import webdriver
import time
from dbhelper_attr import DBHelper
from models import UserModel
import json
import logging
import os
import threading
import random
import traceback
logger = logging.getLogger()
logger_name = ""

relation_list = ['Single','In a relationship','Engaged','Married','In a civil union','In a domestic partnership',
                 'In an open relationship','It''s complicated','Separated','Divorced','Widowed']

def crawl_attrs(user, driver):
    print("crawling %s" % user.url)

    re_dic = get_about(driver, user)

    driver.close()
    driver.quit()
    return re_dic

def get_about(driver, user):

    print(user.url)
    if "profile.php" in user.url:
        url = user.url + "&sk=about"
    else:
        url = user.url + "/about"
    driver.get(url)
    dic = {}
    driver.find_element_by_xpath("//a[@data-testid='nav_edu_work']").click()
    time.sleep(5)
    works = driver.find_elements_by_xpath('//div[@data-pnref="work"]/ul/li/div/div/div/div/div/div[1]')

    #print("work at:")
    dic["work"] = []
    for work in works:
        dic["work"].append(work.text)

    edus = driver.find_elements_by_xpath('//div[@data-pnref="edu"]/ul/li/div/div/div/div/div/div[1]/a')
    #print("educated at:")
    dic["edu"] = []
    for edu in edus:
        dic["edu"].append(edu.text)

    skills = driver.find_elements_by_xpath('//div[@class="fsl fwn fcg"]/a')
    #print("skills:")
    dic["skill"] = []
    if len(skills):
        dic["skill"] = [item.strip() for item in skills[0].text.split("·")]


    driver.find_element_by_xpath('//a[@data-testid="nav_places"]').click()
    time.sleep(2)
    places = driver.find_elements_by_xpath('//div[@data-referrer="pagelet_hometown"]/div/div/ul/li/div/div/div/div/div/div/span/a')
    #print("places:")
    dic["place"] = []
    for place in places:
        dic["place"].append(place.text)
    driver.find_element_by_xpath("//a[@data-testid='nav_contact_basic']").click()
    time.sleep(2)
    contacts = driver.find_elements_by_xpath('//div[@data-referrer="pagelet_contact"]/div/div/ul/li/div')

    # print("contacts:")
    dic["contact"] = {}
    for contact in contacts:
        strs = contact.text.split('\n')
        if strs[0] == "Mobile Phones":
            phones = []
            for str in strs[1:]:
                phones.append(str)
            dic["contact"]["phone"] = phones
        elif strs[0] == "Address":
            dic["contact"]["address"] = ",".join(strs[1:])

    basics = driver.find_elements_by_xpath('//div[@data-referrer="pagelet_basic"]/div/ul/li/div')

    #print("basic info:")
    dic["basic"] = {}
    for basic in basics:
        strs = basic.text.split("\n")
        if strs[0] == "Birthday":
            dic["basic"]["birth"] = strs[1]
        elif strs[0] == "Gender":
            dic["basic"]["gender"] = strs[1]
        elif strs[0] == "Interested In":
            dic["basic"]["interested_in"] = strs[1]
        elif strs[0] == "Languages":
            dic["basic"]["language"] = strs[1]
        elif strs[0] == "Religious Views":
            dic["basic"]["religious"] = strs[1]
        elif strs[0] == "Political Views":
            dic["basic"]["political"] = strs[1]

    driver.find_element_by_xpath("//a[@data-testid='nav_all_relationships']").click()
    time.sleep(2)
    #print("relationship:")

    dic["relationship"] = None
    relation = driver.find_element_by_xpath('//div[@id="pagelet_relationships"]/div[1]/ul/li/div/div')
    print(relation.text)
    txt = relation.text.strip()
    for rel in relation_list:
        if rel in txt:
            dic["relationship"] = rel
            break

    families = driver.find_elements_by_xpath('//div[@id="family-relationships-pagelet"]/div/ul/li/div/div/div/div/div')
    #print("families:")
    dic["family"] = []
    for family in families:
        dic["family"].append(family.text)

    driver.find_element_by_xpath("//a[@data-testid='nav_about']").click()
    time.sleep(2)
    about = driver.find_elements_by_xpath('//div[@id="pagelet_bio"]/div/ul/li/div')
    if len(about):
        dic["about"] = about[0].text
    else:
        dic["about"] = ""
    quote = driver.find_elements_by_xpath('//div[@id="pagelet_quotes"]/div/ul/li/div')
    if len(quote):
        dic["quote"] =quote[0].text
    else:
        dic["quote"] = ""
    print(dic)
    return dic


def run_attr_crawler(driver):
    t_name = threading.current_thread().getName()
    logger = logging.getLogger("log_%s" % t_name)
    dbhelper = DBHelper()
    user = None
    try:
        while not user:
            user = dbhelper.find_user_to_crawl()
            if not user:
                time.sleep(20)
        # print(user.url)
        logger.info("to crawl user %s" % user.username)

        result = crawl_attrs(user, driver)
        dbhelper.save_attributes(user, result)
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


def multi_run_attr_crawler():
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

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--disable-notifications")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    # try:
    cookies = []

    driver.get("https://www.facebook.com/login.php")
    for cookie in cookies:
        driver.add_cookie(cookie)
    while True:
        run_attr_crawler(driver)

if __name__ == "__main__":
    user = UserModel(uid=None, name=None, username=None, url="https://www.facebook.com/profile.php?id=100005132108267", profile=None)
    print(crawl_attrs(user))