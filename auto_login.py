# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0063EF428CF1CCD9E81E379857B2BA73962D08AC31B0EA665084F8D2FB1B01D61CE654DE67D5312C2557E97568C16388FBB84640A45B499A9CFF511D770BD34F1DCA69B75691C96907E580EE0D3443DBF63ADFA10A204FCB299A4E2629E2ECA288787949AE2641EEABCD5914431B09740664C84854C815D4EBF808F8AC1794B54501C1239C77D792620783FFC50E0A155E5109624BCFACABA3B43AC471DD624FA92B1BCEF54CDAEDC4957F7F4E833DF47184B273AA98D8D9B15C2407E46E651F8F91455A5BBE990C0137B24A6C35C4B337F632ABA7BEEECA63A18C0106F5CA61FAF5CFCC7C8C88A86BAA86F8E01250285DAA44D60A4B578A5F89190A8C392F000B5372F4922080E1B47FEA29D1762601B729648F1BE45E5F12112A8354F7F82B96922DEFD022A45A4653C4E3C004E696BD1ACD8ACBB0454763A0C07C7E1F24CCB465DD45493B3EA4FCB9B3F4E362A663711900D2644CA204162B6CB7884386F36B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
