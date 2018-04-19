from selenium import webdriver

import time
import MySQLdb
import random


fbusername = ['rishatapzuj@mail.ru', 'gegamkir1z7@mail.ru']
fbpassword = ['fb2018130', 'fb2018130']


def login():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--disable-notifications")
    #chromeOptions.add_argument('--proxy-server=http://217.12.121.86:80')
    for i in range(0, len(fbusername)):
        driver = webdriver.Chrome(chrome_options=chromeOptions)
        driver.get("https://www.facebook.com/login.php")
    #time.sleep(3)

        driver.find_element_by_id("email").send_keys(fbusername[i])
        driver.find_element_by_id("pass").send_keys(fbpassword[i])
        driver.find_element_by_id("loginbutton").click()

        cookies = driver.get_cookies()
        print(str(cookies))
        time.sleep(30)

        driver.quit()
    # cursor.close()
    # conn.close()


def t_cookies(cookies):
    url = "https://www.facebook.com/selina.joey"
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--disable-notifications")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    # try:

    driver.get("https://www.facebook.com/login.php")
    for cookie in cookies:
        driver.add_cookie(cookie)
    # print(driver.get_cookies())
    driver.get(url + "/friends")

    # except Exception as e:
    #     print(e)
    time.sleep(3)
    driver.close()
    driver.quit()


login()
cnt = 0
# for cookies in cookies_list:
#     print(cnt)
#     t_cookies(cookies)
#     cnt = cnt + 1