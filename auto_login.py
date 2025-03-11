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
    browser.add_cookie({"name": "MUSIC_U", "value": "00434449CAC21F5CDAABB34B565425E5029FE0F4259F1DC86125508CCB954A69A5CD9E3819EA8B0E4A5D751993F1E38762E4837FE7137BDD4FBDC6E91C0225AC1DCC477AB807C8EA2F921B9A90DCD1DE5817BBCC676B261A72F30A4BB8B4C681AFF52460ADD8914FE3C94879D18CC6F5D425A72B625C1B8F34FE4A259318810F0AEE82C48048B954BC30DE5107CBE012A6472B912287D1F852F27D24444301B77E803EFD0A9C39C16A2E65AE2B0BD2B85CEAD9F206263298BAAA2E7FE29BA47212A230CD69D7D132A2F9DF6712DC0326769BC88C034509EE21039E7B7FA54537A628594C83C2D514BABEF1B6B6EAFE060D76F1CB0F23A036CBB78738277B1E38ABFB474B6FA7546D807B56D0684A1D9FD98F10F58198BEC4E263D2A36F42B5FD19720CD689DB92291585CCF4660A74AB639764044E5DA6DE7B32DCC1DFF674D2D08BA70E6276EE3F0D4B501A84AC207064036629D0D63EB9627550D47FD5AE7965"})
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
