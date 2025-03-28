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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E4487D60B39CA778FC19D0BF3494B561ED472E9FE3450DA78C82415BCDE27C0D370B456127A0B7DE22E96CFF3337CD4EC91E9735F6E271A09872DE59AFD45FDFE0922D2DA2A9A125D8F1021D5CABF326056F8E1999A00D967239640869F9F9094080C146515D365CBFF72D66CA1A565E720C9233F493757260552B6C843B2BF3DDF462EEEE2E51E171DEFD1745B4B9292A3F5F4CD0F6E149CDF5CAB06B4F42D5D2B81E3FA1AFB30A4DAC737FA5CAA3B75EE67A0A6D46C46A3B98C323356ADD133A3BA7B7E2FEE4C028AE24A530922083A7A1FD4C1674CAB1768D3D4E8B324993175A4B640678C27CAB53441E7E6BD38A5074A670E8D7730F978442427A7ABC8088ECF3AEEAAEE4FF92C2902D5A95D7959D8093A3902886493B7DAA9F43E5424AC57AF8C516F1AAE0F31641786309DCE9FDC5CA20780F02B58B90CED190033411666CF313BF9E7AA2F3B8F41CE28D2413392A8B335592D79280E82D3D4A1A8F59"})
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
