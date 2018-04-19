from selenium import webdriver
import time


def get_new_cookie(username, password):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--disable-notifications")

    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.get("https://www.facebook.com/login.php")
    # time.sleep(3)
    driver.find_element_by_id("email").send_keys(username)
    driver.find_element_by_id("pass").send_keys(password)
    driver.find_element_by_id("loginbutton").click()

    cookies = driver.get_cookies()
    print(str(cookies))
    time.sleep(30)

    driver.quit()