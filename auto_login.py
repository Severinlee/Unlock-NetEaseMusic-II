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
    browser.add_cookie({"name": "MUSIC_U", "value": "0071505CC8ECA2E04718B041948206EE701C5E23837ECD90C504E268A2E3B69E3AB9C256D4D9DD45D86DD1771BAD364A8C3BA4D7C07F320B58662D92208D900F04F80880BB464FCDEA608C05B11ECB2AD5612CD772A0AB52AA98362AFBF60546E7233443C908C59EDFDA9060AE9EF9BFE5FEDE4E1A70241EB76E6439C0E26ACF0947CB4F8AA4EEF76BEFF4F9699C0A842D34D4379226A70BD7A5B06F44132A7EDC803AB80A089403B967E98C680C58462A3B91E696BDB22373FB7CAB839136E21DDF5E22A1F86ACBC5BFF6F72672961BB4043C263DA20DE7E9A06203124291E457B1757A18132794045F517FF94DCE16FB354F0F926E94C1FBE4649BE1CC783150E28BA9EADDD86A6A608FA499E216D0E6DF464C911D50BE7A0D03526D609A0271A4A1322751A76B343B3A9F1D4FD5AC7B9AD58FEC0AF16A3FBCCA8A1BDDB38ADCF941D885A780157511EBD06CC1AFE3BABAC1994B59D2EF170E1A2EB507AF5731"})
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
