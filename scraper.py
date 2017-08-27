#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import platform
import time
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Using the right PhantomJS for the corresponding OS
if platform.system() == "Windows":
    PHANTOMJS_EXE = "./PhantomJS/phantomjs.exe"
else:
    PHANTOMJS_EXE = "./PhantomJS/phantomjs"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " + \
             "AppleWebKit/537.36 (KHTML, like Gecko) " + \
             "Chrome/55.0.2883.87 Safari/537.36"

URL_LOGIN = "http://datalogger.capnuocnhabe.vn"
# URL_LOGIN = "http://113.161.69.85:1802/Login.aspx"


def site_log_in(driver):
    # METHOD 1
    # --------
    driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_ucLogin1_Login1_UserName']").send_keys("sawaco")
    driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_ucLogin1_Login1_Password']").send_keys("123456")
    driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_ucLogin1_Login1_LoginButton']").click()

    # METHOD 2
    # --------
    # from selenium.webdriver.common.keys import Keys
    # from selenium.webdriver import ActionChains
    # username_field = driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_ucLogin1_Login1_UserName']")
    # password_field = driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_ucLogin1_Login1_Password']")
    # actions = ActionChains(driver).click(username_field).send_keys("sawaco")\
    #                               .click(password_field).send_keys("123456")\
    #                               .send_keys(Keys.RETURN)
    # actions.perform()

    # METHOD 3
    # --------
    # wait = WebDriverWait(driver, 10)
    # username = wait.until(EC.element_to_be_clickable(
    #     (By.XPATH, "//input[@name='ctl00$ContentPlaceHolder1$ucLogin1$Login1$UserName']")))
    # username.send_keys("sawaco")
    # password = wait.until(EC.element_to_be_clickable(
    #     (By.XPATH, "//input[@name='ctl00$ContentPlaceHolder1$ucLogin1$Login1$Password']")))
    # password.send_keys("123456")
    # login_btn = driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_ucLogin1_Login1_LoginButton']")
    # login_btn.click()


def main():
    # Use PhantomJS to browse the page
    caps = webdriver.DesiredCapabilities.PHANTOMJS
    caps['phantomjs.page.settings.userAgent'] = USER_AGENT
    driver = webdriver.PhantomJS(executable_path=PHANTOMJS_EXE, desired_capabilities=caps)

    driver.get(URL_LOGIN)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ucLogin1_Login1_LoginButton")))
    site_log_in(driver)
    wait.until(EC.presence_of_all_elements_located((By.ID, "RAD_SLIDING_PANE_TEXT_RadSlidingPane2")))
    driver.maximize_window()

    driver.save_screenshot('screen_shoot.png')
    driver.close()


if __name__ == "__main__":
    main()
else:
    print("This Python script is to be called as main(), not as the module ", __name__ + ".")
