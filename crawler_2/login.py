from selenium import webdriver
from config import *
import time
#login函数用于登录facebook和保持登录状态
# 参数browser为浏览器
# #
def login(browser,cookies):
    browser=webdriver.Firefox()
    facebook_login_url = "https://www.facebook.com/login.php"
    if len(cookies)==0:
        browser.get(facebook_login_url)
        browser.find_element_by_xpath('//*[@id="email"]').send_keys(USERNAME)#找到Facebook登录网页的用户名输入处
        browser.find_element_by_xpath('//*[@id="pass"]').send_keys(PASSWD)#密码输入口
        browser.find_element_by_xpath('//*[@id="loginbutton"]').click()#点击登录按钮
        cookies=GetCookies(browser)
    else:
        for cookie in cookies:
            browser.add_cookie(cookie)
        print(browser.get_cookies())
        browser.get(facebook_login_url)

#获取当前浏览器的cookies
def GetCookies(browser):
    #browser=webdriver.Firefox()
    cookies=browser.get_cookies()
    print(type(cookies))
    print(str(cookies))
    return cookies
browser=webdriver.Firefox()
login(browser)