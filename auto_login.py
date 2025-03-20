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
    browser.add_cookie({"name": "MUSIC_U", "value": "0077AF52C8B7C246D70D479692140A6588A1B9316A24F727FD5BC193DB5B24CAAC34ED928D92CFE2606799293CD553E7299EC9FEA436C3AAD79E5C61D238F974DAC13F7DB9BA31E015185FBDD4661356320191B61F9A56B9E9F4A323A442D9A6D483BB18BD913F5EC95C4AFDDC130A68498EB4C141EBAD676DDD5D3DAE3B476A216A59FE67F1A4C7A79930781146FE4B2FCA8B2F9E3649DA55D6905AAE3A9AD4B47D89EE5AB3681AAA49F62CB8BB29EBA78914BD6E72E2DA8C6A9137D5A22AAB5A62CB3981EB17BE5D67BB4C8BEA8A7DCD81995CC4751F88672CF7B974DE11904EBC28D4A484EDB65A4A05BEABFDE934AB4D17AC2EFE2426F82C396AF82E3A537932489B777473A3BB26A2BC15AC39C9837116647A4F2E510685D9617D642830859C6E321D6A5216BA651041A8068A5BEAE681BB0DE68A33173C9E9C60A4D7417237B9F029A0AD98229731D7DBA59CDB5CA163840F655F666ACB2B29912B005F01"})
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
