from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import logging
import os
logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)

file_formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
cons_formatter = logging.Formatter("%(process) : %(levelname)-8s %(message)s")

fh = logging.FileHandler("log.log")
ch = logging.StreamHandler()

fh.setFormatter(file_formatter)
ch.setFormatter(file_formatter)

logger.addHandler(fh)
logger.addHandler(ch)

def visit():
    cookie_dic = {}
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--disable-notifications")
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    # driver.get("https://www.facebook.com/login.php")
    # driver.find_element_by_id("email").send_keys(username)
    # driver.find_element_by_id("pass").send_keys(password)
    # driver.find_element_by_id("loginbutton").click()
    # #driver.get("https://www.facebook.com/juliancha.julian?fref=pb&hc_location=friends_tab")
    # cookies = driver.get_cookies()
    # time.sleep(5)
    cookies = [{'domain': '.facebook.com', 'httpOnly': False, 'name': '_js_reg_fb_ref', 'path': '/', 'secure': True, 'value': 'https%3A%2F%2Fwww.facebook.com%2Flogin.php'}, {'domain': '.facebook.com', 'expiry': 1516001667, 'httpOnly': False, 'name': 'wd', 'path': '/', 'secure': True, 'value': '1036x675'}, {'domain': '.facebook.com', 'expiry': 1578468860.767658, 'httpOnly': True, 'name': 'datr', 'path': '/', 'secure': True, 'value': '9x5TWjf--2UlNXPTlCzQJQav'}, {'domain': '.facebook.com', 'expiry': 1523172865.671106, 'httpOnly': True, 'name': 'xs', 'path': '/', 'secure': True, 'value': '42%3ASmJNEiGSJJuUcw%3A2%3A1515396864%3A-1%3A-1'}, {'domain': '.facebook.com', 'expiry': 1523172865.671058, 'httpOnly': False, 'name': 'c_user', 'path': '/', 'secure': True, 'value': '100023787982804'}, {'domain': '.facebook.com', 'expiry': 2146116886, 'httpOnly': False, 'name': 'presence', 'path': '/', 'secure': True, 'value': 'EDvF3EtimeF1515396868EuserFA21B23787982804A2EstateFDutF1515396868474CEchF_7bCC'}, {'domain': '.facebook.com', 'httpOnly': True, 'name': 'reg_fb_gate', 'path': '/', 'secure': True, 'value': 'https%3A%2F%2Fwww.facebook.com%2Flogin.php'}, {'domain': '.facebook.com', 'httpOnly': True, 'name': 'reg_fb_ref', 'path': '/', 'secure': True, 'value': 'https%3A%2F%2Fwww.facebook.com%2Flogin.php'}, {'domain': '.facebook.com', 'expiry': 1523172865.671221, 'httpOnly': True, 'name': 'pl', 'path': '/', 'secure': True, 'value': 'n'}, {'domain': '.facebook.com', 'expiry': 1523172865.671157, 'httpOnly': True, 'name': 'fr', 'path': '/', 'secure': True, 'value': '0gmmAyWFWKwz8NDDm.AWWNMwPj6uIlDfBEpygG-23q9aI.BaUx73.ig.AAA.0.0.BaUx8A.AWWG8n7b'}, {'domain': '.facebook.com', 'expiry': 1516001664, 'httpOnly': False, 'name': 'dpr', 'path': '/', 'secure': True, 'value': '1.25'}, {'domain': '.facebook.com', 'expiry': 1578468865.670949, 'httpOnly': True, 'name': 'sb', 'path': '/', 'secure': True, 'value': 'AB9TWrVWFQf-rE7oHCqWM2bb'}]

    driver.get("https://www.facebook.com/login.php")
    for cookie in cookies:
        driver.add_cookie(cookie)
    print(driver.get_cookies())
    cnt = 0
    while cnt < 999999:
        driver.get("https://www.facebook.com/emygaild.santiago")
        driver.find_element_by_xpath('//a[@data-tab-key="friends"]').click()
        print(cnt)
        time.sleep(30)
        cnt = cnt + 1

    #driver.get("https://www.facebook.com/mjmipa.aquinooooo?hc_location=friend_browser&fref=pymk")


    driver.close()

# try:
#     cnt = 0
#     while True:
#         print(cnt)
#         cnt = cnt + 1
# except Exception as e:
#     print("Oops!")
#coding=utf-8
import threading
from time import ctime,sleep


def music(func):
    for i in range(2):
        print("I was listening to %s. %s" %(func,ctime()))
        sleep(1)

def move(func):
    for i in range(2):
        print("I was at the %s! %s" %(func,ctime()))
        sleep(5)

threads = []
t1 = threading.Thread(target=music,args=(u'爱情买卖',))
threads.append(t1)
t2 = threading.Thread(target=move,args=(u'阿凡达',))
threads.append(t2)

# if __name__ == '__main__':
#     cnt = 1
#     try:
#         while True:
#             print(cnt)
#             cnt = cnt + 1
#     except KeyboardInterrupt as e:
#         print(0)
print(type(os.getpid()))