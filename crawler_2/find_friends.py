from selenium import webdriver
from config import *
from login import login


def find_friends(browser):
    browser = webdriver.Firefox()
    login(browser)
    friends = browser.find_element_by_xpath('//*[@id="navItem_1572366616371383"]/a/div')
    friends.click()
    

