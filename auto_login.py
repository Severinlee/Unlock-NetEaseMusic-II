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
    browser.add_cookie({"name": "MUSIC_U", "value": "004B55C05FD22A9738EE220549D19F46C8B4CE2F1EE2905ED579485D006D6B754E2730C4587B5092BF92EA8F1D6F9095FB7C7C81E9912189D51FB0ADB0A994BBA71013D8E190A824488A8B5346B4BABDDB054964EA715D5D1A6C8A455071D1737CD157ED205726257CF39FDC655BAADFF7FEFAF4548BEECB902B5EEC9A12FE6DEA8534639CA88925C9429E904A30749D061F3550629B4D2673692DF31518E9EAB909EFD71976593052F678CC2FFC9AD819A08C5D25469687F5356FCED4A5105A1CD6EDBDA366FFE455FA001866BE697488237F5BE09E75DC2E441C4B0451A31C6E4BB6194860877247C54362B609AE8A7AF3D52CA0259B6C6E5A760C88B33F1A087D955A77968A533EF351A201DB0E1828DC2A5063362F9ACFAC979F2005E3B83ACEF96558C44DD0B35BF4D1D1AA89B2BC57123DB6D88D535872A6BCC9BC1F6330F2C9220D3FA47869B47A7D3D83AB181EB5BA61E956EF2B5961EB998C87F84373"})
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
