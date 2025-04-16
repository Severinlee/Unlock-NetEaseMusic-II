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
    browser.add_cookie({"name": "MUSIC_U", "value": "0036CE80E9737D7288EC2A87643D2EE3452F690727309A1C2698B9F1E69EE905A260FE3E3C901CE9AAA53F9AB51940F485634D05F717D35EBB7F875A58AF25DC977B5CF2B3C3A5E896EC23565F3E54C14A21D6DE5A7E30D863A92063F9CB88B41006EC9E881EFCF156F3B1CD0DFB9EC05A4F9E523520189CFC082AAE83FAA464ACCE98732712819F6D5A0A32272331DDA08CA6030507DD3FDF48ED69286E77F97D5CC82F1306F285B5CEA0C344E1C043340924265E1839148192C14A98C65236A0E3B214C035458A44ACB8A0E74430188B7675C0728DBEA4E0DA316339E4848FF011BA951C3A6B414EC1B03DE746A235D179B23CE60704CC585A0ED369B53C022E9FEA4CC766C98DF3F1BE1F0ABDD4D072F192293315A1FEC922B93A06D6E1B9D617CF6699A3FCEF233521DDF5D0547121B3387F45B8288A36956EB9F15EEDED4691CBD36B0AE943733AEE974403E1114873F23BBBE47F14DD714E33E6CF8786EF"})
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
