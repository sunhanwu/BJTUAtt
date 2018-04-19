from selenium import webdriver
from config import *
from login import login
import time


def find_friends(browser):

    login(browser)
    friends = browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[1]/div/div/div/div/div/div/div[3]/div[2]/ul/li[4]/a/div')
    friends.click()

    time.sleep(3)
    allfriend=browser.find_element_by_xpath('//*[@id="pagelet_bookmark_seeall"]/div/div/div[1]/div/div[1]/div/a[2]')
    allfriend.click()


    cnt = 1
    body = browser.find_element_by_tag_name("body")
    last = body.size['height']
    while True:
        script = "window.scrollTo(0, %d);" % (body.size['height'] + 100)
        browser.execute_script(script)
        # print(script)
        time.sleep(1)
        now = body.size['height']
        # print(now)
        if cnt % 10 == 0:
            if now == last:
                break
            last = now
        cnt = cnt + 1

    friends=browser.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div/ul/*')
    print(type(friends))
    with open('friend.csv','e') as f:
        for friend in friends:
            f.writelines(friend.div.a.herf)
browser = webdriver.Firefox()
find_friends(browser)



