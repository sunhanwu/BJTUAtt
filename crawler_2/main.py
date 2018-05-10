from selenium import webdriver
from config import *
from login import login
#定义一个浏览器
browser=webdriver.Chrome()
login(browser)
