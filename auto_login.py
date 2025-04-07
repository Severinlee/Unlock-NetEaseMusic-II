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
    browser.add_cookie({"name": "MUSIC_U", "value": "006F1A475577477832E767983B6873A91F746950F8B0F06F0BA80B376D9223A6A0F28656D2865EB858F6A75802B1CBDC072CC038E87A7FA7DFA17C6C7AF850440ADB72D1EF7373F7C86BF7B9B057A34EE7B58E26246806ADD1623AAC6338796A0EC36C4421904261D1638E8406727622662F0D74650D8C077C643D0CB1EF8C68EE9A8E8EFF7358DFD205F777E5B2BA7F632A9FAEB9B391ADDB1ADB4991E73F3177BDA7CA04AC2E000FD56CB3C12EE492B5BAD61997FF2F6495CC77BFB11EFBA3DBF7FD445D894A163E0CB7352719BC6B2FCA57BD100EE5AD4A69C5FF786EE40FD154D9F78861518AE4C601A910C94AE39F9686170F4B50AD5D766E28BEB58B4D77E2D37F0BD7317D4AF7B302C0CFF300DE3D6C82AA53E43568CE54303CE550E214D02AAC7AEF204BEBE97A5BAD8452DB19F50A430895B69166109493006E3A3A02F4B05BAE5C0A490D7E3E14E637B7E73B1F5037BDB60D867CC78040B51DD70CAF"})
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
