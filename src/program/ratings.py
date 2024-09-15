import time
import os
from selenium.webdriver.common.by import By
from program.helpers.logging import logger

def get_rating(driver, company):
    logger.info(f"Getting rating for {company}")
    search = f"https://www.google.com/search?q={company}+glassdoor"
    driver.get(search)

    attempt = 1
    max_attempts = 5
    rating_msg = None
    while attempt <= max_attempts:
        try:
            rating_msg = driver.find_element(By.XPATH, '//span[text()[contains(., "Rating")]]').text
            break
        except:
            logger.error(f"Error getting rating. Attempt {attempt} of {max_attempts}")
            time.sleep(2)
            attempt += 1
    if attempt == 5:
        logger.error(f"Could not get rating for {company}. Skipping...")
        return [company, 0]
    else:
        rating = float(rating_msg.split(" ")[1].replace(",", "."))
        logger.info(f"Rating for {company}: {rating_msg}")
        return [company, rating]
