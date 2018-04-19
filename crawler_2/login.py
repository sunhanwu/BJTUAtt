from selenium import webdriver
from config import *
import json
import os
#login函数用于登录facebook和保持登录状态
# 参数browser为浏览器
# #
def login(browser):
    #browser=webdriver.Firefox()
    facebook_login_url = "https://www.facebook.com/login.php"
    cookies=[]
    #try:
    #读取cookies.txt文件中的cookies，如果cookies过期的话，就用账号密码登录一遍
    with open('cookies.txt','r') as f:
        for line in f:
            cookie=eval(f.readline())
            cookies.append(cookie)
    print(type(cookies))
    browser.get(facebook_login_url,cookies=cookies)
    # for cookie in cookies:
    #     browser.add_cookie(cookie)
    # except Exception:
    #     browser.get(facebook_login_url)
    #     browser.find_element_by_xpath('//*[@id="email"]').send_keys(USERNAME)#找到Facebook登录网页的用户名输入处
    #     browser.find_element_by_xpath('//*[@id="pass"]').send_keys(PASSWD)#密码输入口
    #     browser.find_element_by_xpath('//*[@id="loginbutton"]').click()#点击登录按钮
    #     cookies=GetCookies(browser)
    #     os.remove('cookies.txt')
    #     with open('cookies.txt','w') as f:
    #         for cookie in cookies:
    #             f.write(str(cookie)+'\n')
    #     print("cookies更新",cookies)
#获取当前浏览器的cookies
def GetCookies(browser):
    #browser=webdriver.Firefox()
    cookies=browser.get_cookies()
    #print(type(cookies))
    print(str(cookies))
    return cookies
browser=webdriver.Firefox()
login(browser)