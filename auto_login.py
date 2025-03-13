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
    browser.add_cookie({"name": "MUSIC_U", "value": "001F896335A3209DE6DF2F93DD1095A0A7CDFA32B06D831C53CFADBC18CAE39A34B923253AD8B7B22C6853A144B4CD4A73B58E80EC6755F221A95AECA175FCA8D561A488AAA25BED6609FCA31A5B330406278FB9490302E7573E860DF835D313C69844CD5BC3AD8EE55B5811BCF1BA4696C98F271AFB6D5447B07B9C83D2C68EB12DD88E12C4A6C335C756B4516AFED7DC870DDB0935381F6ACF8590C6203D068DB2FF8E93D9BD1A11EF4E973F7968DEE4AFC6694CC44B17311705AF9C7727867920B3F55519416354FA92DF86C13BA0EA0C1CA6E0E863591EB5874E71A505C71AC83A480C4E651A3A3DD707C9472A8088D4D53CA0D6D3CA8AFCA9E123EFD32492E91414095A9EDF3D078938DCFEEB048C4FDCE8E5F7076BDFB234401BCFB9740B6EB9CD4C395F482163D6D76FFDF84D473102917D10E548D75BDC012BB48A9CE46AD27D6279239445DA8C1F34707728D6810DB7D9DF7F3ECC9B3E5C870C454D89"})
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
