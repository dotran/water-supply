#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import platform
import time
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

# URL_LOGIN = "http://datalogger.capnuocnhabe.vn"
URL_LOGIN = "http://113.161.69.85:1802/Login.aspx"
ACCOUNT = {'id': "sawaco", 'pw': "123456"}
URL_LOGGER = "http://113.161.69.85:1802/Consumer/Logger/Daily_Monthly.aspx"
START_DATE = '01/09/2017'
END_DATE   = '05/09/2017'
XNTD = ["39 Ben Van Don",
        "65 BEN VAN DON",
        # "90 BEN VAN DON",
        # "BEN VAN DON_NGUYEN KHOAI",
        # "CALMETTE - BEN VAN DON",
        # "CAU HIEP PHUOC",
        # "CAU RACH ONG 1",
        # "Cau Rach Ong 2",
        # "CAU TAC BEN RO",
        # "CTY PT CN TAN THUAN",
        # "D1000 Huynh Tan Phat",
        # "D300 Cau Ba Chiem",
        # "D600 Cau Ong Lon",
        # "D600 NVLinh_NHTho",
        # "KCN HIEP PHUOC",
        # "KCX TThuan",
        # "LONG THOI - NHON DUC",
        # "NGUYEN BINH",
        # "NHTho_PHLau",
        # "NVLinh_NLBang",
        "VUON UOM BOO",
        # "Vuon uom Tan Thuan",
        "D1000 Huynh Tan Phat (ÐC)",
        # "D300 Cau Ba Chiem (ÐC)",
        # "D600 NVLinh_NHTho (ÐC)",
        # "NHTho_PHLau (ÐC)",
        # "NVLinh_NLBang (ÐC)",
        # "Vuon uom BOO (ÐC)",
        # "Vuon uom Tan Thuan (ÐC)",
]

XNTD = ["102 LE QUOC HUNG"]


class Timer(object):
    """A simple facility to measure duration from the previous timing.

    Init:       timer = Timer()
    Measure:    timer("Something has done")
    Output:     Something has done in x.x sec.
    """

    def __init__(self):
        self.log = time.time()

    def __call__(self, msg=None):
        if not msg:
            self._save_clock()
            return
        print("{} in {:.1f} sec.".format(msg, self._until_now()))

    def _save_clock(self):
        self.log = time.time()

    def _until_now(self):
        interval = time.time() - self.log
        self._save_clock()
        return interval


def site_log_in(driver, account):
    timer = Timer()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ucLogin1_Login1_LoginButton")))
    timer("Login page loaded")

    # METHOD 1
    # --------
    driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_ucLogin1_Login1_UserName']").send_keys(account['id'])
    driver.find_element_by_xpath("//input[@id='ContentPlaceHolder1_ucLogin1_Login1_Password']").send_keys(account['pw'])
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

    wait.until(EC.presence_of_all_elements_located((By.ID, "RAD_SLIDING_PANE_TEXT_RadSlidingPane2")))
    driver.maximize_window()
    timer("Logged in successfully")


def get_locations_list(driver):
    """Return the list of all locations/meters available in the dropdown.
    """
    elem = rewind_dropdown_list(driver, 1)
    locations = []
    while True:
        loc = get_highlighted_location(driver)
        if locations and loc == locations[-1]:
            break
        locations.append(loc)
        elem.send_keys(Keys.ARROW_DOWN + Keys.ENTER)
    rewind_dropdown_list(elem, len(locations))
    return locations


def get_highlighted_location(driver):
    """Read the name of the location/meter that are
    currently highlighted in the dropdown list.

    Example:
    value = {"logEntries":[],"value":"Vuon uom Tan Thuan (ÐC)","text":"Vuon uom Tan Thuan (ĐC)","enabled":true,"checkedIndices":[],"checkedItemsTextOverflows":false}
    """
    value = driver.find_element_by_xpath(
        "//input[@id='ctl00_ContentPlaceHolder1_ucDailyReportConsumer_cboSites_ClientState']") \
        .get_attribute("value")
    val = value.split(',')[1].split(':')[1].strip('"')
    text = value.split(',')[2].split(':')[1].strip('"')
    return {'value': val, 'text': text}


def rewind_dropdown_list(driver, num_steps):
    """Go to the beginning of the dropdown list.
    """
    element = driver.find_element_by_xpath(
        "//input[@id='ctl00_ContentPlaceHolder1_ucDailyReportConsumer_cboSites_Input']")
    element.click()
    element.send_keys(Keys.ARROW_DOWN)
    for i in range(num_steps):
        element.send_keys(Keys.ARROW_UP)
    element.send_keys(Keys.ENTER)
    return element


def select_a_location(driver, list_length, location):
    """Select a location/meter from the dropdown list.
    """
    elem = rewind_dropdown_list(driver, list_length)
    elem.click()

    previous_loc = None
    while True:
        current_loc = get_highlighted_location(driver)
        # print(current_loc)
        if current_loc == previous_loc:
            print("Couldn't find the requested location/meter.")
            return False
        if location in current_loc.values():
            return True
        previous_loc = current_loc
        elem.send_keys(Keys.ARROW_DOWN + Keys.ENTER)


class TableWait(object):

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def __enter__(self):
        tables = self.driver.find_elements_by_xpath("//table[@id='ctl00_ContentPlaceHolder1_ucDailyReportConsumer_grv_ctl00']")
        if len(tables) == 0:
            self.begin = True
        else:
            self.begin = False
            self.old_table = tables[0]

        # Click on the Xem button
        self.driver.find_element_by_xpath(
            "//input[@id='ctl00_ContentPlaceHolder1_ucDailyReportConsumer_btnView_input']").click()

    def __exit__(self, *_):
        if self.begin:
            # WebDriverWait(self.driver, self.timeout).until(
            #     EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_ucDailyReportConsumer_grv_ctl00")))
            wait_for(self.table_has_shown, self.timeout)
        else:
            wait_for(self.table_has_updated, self.timeout)

    def table_has_shown(self):
        tables = self.driver.find_elements_by_xpath("//table[@id='ctl00_ContentPlaceHolder1_ucDailyReportConsumer_grv_ctl00']")
        return len(tables) > 0

    def table_has_updated(self):
        new_table = self.driver.find_element_by_xpath("//table[@id='ctl00_ContentPlaceHolder1_ucDailyReportConsumer_grv_ctl00']")
        return new_table.id != self.old_table.id


def wait_for(condition_function, timeout):
    start_time = time.time()
    while time.time() < start_time + timeout:
        if condition_function():
            print("Waited successfully in {:.1f} sec.".format(time.time() - start_time))
            return True
        else:
            time.sleep(0.1)
    raise Exception("Timeout {} sec waiting for {}.".format(timeout, condition_function.__name__))
    # print("  Timeout waiting for table update.")
    # return False


def main():
    # Use PhantomJS to browse the page
    caps = webdriver.DesiredCapabilities.PHANTOMJS
    caps['phantomjs.page.settings.userAgent'] = USER_AGENT
    driver = webdriver.PhantomJS(executable_path=PHANTOMJS_EXE, desired_capabilities=caps)

    driver.get(URL_LOGIN)
    site_log_in(driver, ACCOUNT)

    # Now that you are logged in, go to the page of interest
    driver.get(URL_LOGGER)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_ucDailyReportConsumer_btnView_input")))

    element = driver.find_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder1_ucDailyReportConsumer_dtmStart_dateInput']")
    element.clear()
    element.send_keys(START_DATE)

    element = driver.find_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder1_ucDailyReportConsumer_dtmEnd_dateInput']")
    element.clear()
    element.send_keys(END_DATE)

    locations = get_locations_list(driver)
    # for i in locations:
    #     print(i)

    for i, loc in enumerate(XNTD):
        print("\nLocating '{}' ...".format(loc))
        if loc not in [item['value'] for item in locations] and \
                loc not in [item['text'] for item in locations]:
            print("** '{}' not found.".format(loc))
            continue
        if select_a_location(driver, len(locations), loc):
            print("OK.")
            table_wait = TableWait(driver, timeout=30)
            try:
                with table_wait:
                    pass
            except Exception as msg:
                print("** Omitting '{}': {}".format(str(loc), msg))
                continue
            driver.save_screenshot('screenshoot_{}_{}.png'.format(i, loc))

            element = driver.find_element_by_xpath(
                "//*[@id='ctl00_ContentPlaceHolder1_ucDailyReportConsumer_grv_ctl00__0']/td[2]")
            print("  --> " + element.text)

    driver.close()


if __name__ == "__main__":
    main()
else:
    print("This Python script is to be called as main(), not as the module ", __name__ + ".")


"""
90 BEN VAN DON
    du lieu chi tiet trong Bang:
        http://113.161.69.85:1802/Consumer/Logger/DetailTable.aspx?si=90 BEN VAN DON&dt=0
    ko co Ap luc, toan 0.00, nhung trong trang logger co gia tri Ap luc Min Max trong Ngay
"""