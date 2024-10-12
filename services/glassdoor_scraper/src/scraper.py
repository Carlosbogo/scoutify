import time
import random
from seleniumbase import Driver
from seleniumbase.undetected.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.helpers import format_reviews_string
from utils.logging import logger


def get_companies_in_page(driver: Driver) -> list[WebElement]:
    time.sleep(random.uniform(3.5, 5))
    companies = driver.find_elements(By.XPATH, "//div[@data-test='employer-card-single']")
    return companies


def get_company_locations(driver: Driver,company: WebElement):
    # Go to the location url
    locations = company.find_element(By.XPATH, ".//span[@data-test='employer-location']")
    children = locations.find_elements(By.XPATH, ".//*")
    if not children:
        # If there is no location url, we get the only location from the company card
        # It starts with "Sede en " so we remove it
        return [(locations.text[8:], "No rating")]
    else:
        locations_url = children[0].get_attribute("href")
    default_window = driver.current_window_handle
    time.sleep(random.uniform(0.5, 1.2))
    driver.switch_to.new_window("window")
    time.sleep(random.uniform(0.4, 1.1))
    driver.uc_open_with_reconnect(locations_url)
    time.sleep(random.uniform(0.3, 1.0))
    if driver.current_window_handle == default_window:
        time.sleep(random.uniform(0.5, 1.5))
        driver.switch_to_window(driver.window_handles[0])
    try:
        driver.find_element(By.ID, "HardsellOverlay")
        driver.execute_script(
            """
                document.querySelector('#HardsellOverlay > div').remove();
                document.querySelector('body').style.overflow = 'auto';
                document.querySelector('html').style.overflow = 'auto';
        """)
    except NoSuchElementException:
        logger.info("No HardsellOverlay found")
        pass
    # Get the locations
    locations = [loc.text for loc in driver.find_elements(By.XPATH, "//a[@class='css-4g6ai3 e1ecbt1s4']")]
    ratings = [rating.text for rating in driver.find_elements(By.XPATH, "//p[@class='css-1l1p60u e1ecbt1s2']")]
    location_info = list(zip(locations, ratings))
    driver.close()
    driver.switch_to_window(default_window)
    time.sleep(random.uniform(0.3, 1.1))

    return location_info


def get_company_info(driver: Driver, company: WebElement, get_locations: bool = False):
    time.sleep(random.uniform(0.1, 0.3))
    company_name = company.find_element(By.XPATH, ".//h2[@data-test='employer-short-name']").text
    try:
        company_rating = company.find_element(By.XPATH, ".//span[@data-test='rating']").text.replace(",", ".")
    except NoSuchElementException:
        company_rating = "0.0"
    review_string = company.find_element(By.XPATH, ".//h3[@data-test='cell-Reviews-count']").text
    review_count = format_reviews_string(review_string)

    logger.info(f"Company: {company_name} - Rating: {company_rating} - Reviews: {review_count}")

    if get_locations:
        locations = get_company_locations(driver, company)
        return [company_name, company_rating, review_count, locations]

    return [company_name, company_rating, review_count]


def click_next_page(driver: Driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-test='pagination-next']"))
        ).uc_click()
    except TimeoutError:
        logger.error("Next page button not found")
        raise Exception("Next page button not found")
