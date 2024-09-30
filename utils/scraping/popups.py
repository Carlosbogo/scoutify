from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils.logging import logger


def reject_google_privacy_popup(
    driver: webdriver, reject: bool = True
) -> None:
    deny_cookies_button = driver.find_element(
        By.XPATH, '//button[.//div[contains(text(), "Rechazar todo")]]'
    )
    driver.implicitly_wait(10)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(deny_cookies_button)
    ).click()
    logger.info("Google Privacy Popup rejected.")


def handle_glassdoor_cookies_popup(
    driver: webdriver, accept: bool = True
) -> bool:
    try:
        accept_cookies_button = driver.find_element(
            By.ID, 'onetrust-accept-btn-handler'
        )
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(accept_cookies_button)
        ).click()
        logger.info("Glassdoor Cookies Popup accepted.")
        return True
    except Exception as e:
        logger.error(f"Error handling Glassdoor Cookies Popup: {e}")
        return False
