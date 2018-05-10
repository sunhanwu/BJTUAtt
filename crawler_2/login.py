from selenium import webdriver
from config import *
import os
import time
#login函数用于登录facebook和保持登录状态
# 参数browser为浏览器
#
# #
def login(browser):
    #browser=webdriver.Firefox()
    facebook_login_url = "https://www.facebook.com/login.php"
    cookies=[]
    try:
    #读取cookies.txt文件中的cookies，如果cookies过期的话，就用账号密码登录一遍
        print('try add cookies')
        with open('cookies.txt','r') as f:
            for line in f:
                cookie=eval(f.readline())
                cookies.append(cookie)
        print(type(cookies))
        print(cookies)
        browser.get(facebook_login_url)
        browser.delete_all_cookies()
        for cookie in cookies:
            browser.add_cookie(cookie)
        time.sleep(5)
        browser.get(facebook_login_url)
    except Exception:
        print('except,try login by username and passwd ')
        browser.get(facebook_login_url)
        username=browser.find_element_by_xpath('//*[@id="email"]')#找到Facebook登录网页的用户名输入处
        username.send_keys(USERNAME)
        passwd=browser.find_element_by_xpath('//*[@id="pass"]')
        passwd.send_keys(PASSWD)#密码输入口
        button=browser.find_element_by_xpath('//*[@id="loginbutton"]')
        button.click()#点击登录按钮
        print('click the button')
        cookies=GetCookies(browser)
        os.remove('cookies.txt')
        with open('cookies.txt','w') as f:
            for cookie in cookies:
                f.write(str(cookie)+'\n')
        print("cookies更新",cookies)


#获取当前浏览器的cookies
def GetCookies(browser):
    cookies=browser.get_cookies()
    print(str(cookies))
    return cookies
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("--disable-notifications")
prefs = {"profile.managed_default_content_settings.images": 2}
chromeOptions.add_experimental_option("prefs", prefs)
browser=webdriver.Chrome(chrome_options=chromeOptions)
login(browser)