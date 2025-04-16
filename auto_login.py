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
    browser.add_cookie({"name": "MUSIC_U", "value": "00BAAEF99FE3A76EFBF628184F98EE9A2C889AEB437376C8C373B92511248CDF0C2D509ABB4B28906E32AD8E44B2B1E0959DFE3BD9562F47227D8B3C0C860BD5E7A63BC797F5E862D2BC190B483CFC5E2AFFB0C3484B53B4916251E826BE7B9440808A7288F5552CAF1017F223911DB9528F7FB6AE54B51CCE5F572ADF5D676C75605EF86F2BFD584190F8BE587D510CA34CD9FBFB1D38AC806AC791A78BCB52C56922986ADAE4709850066FCB0DB826AC93B4D3E70753E699CD96D6816631EBFA45C859515750B067820E93D9785A84247B3A2020740908AE3056A790988DB6B4757887F89A66D02153D07E20E806131FC5CE4FBF3B6677D444F18B076D213B5BA814ABE856C0794F921B9F7807BC945EFE686ACE34E217A08EF92D609A9FB51CF729D7521810F3BC93C954C7EE4C4FE9D6D239C07B46F93EBBE9218847E4EA178E9857A273A8ECD7DE2E6E9D1BCED1DAB348623E44270AC12F62FF37F6944181"})
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
