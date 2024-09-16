import time
import os
from selenium.webdriver.common.by import By
from program.helpers.logging import logger


def get_text(driver, text, max_attempts=5):
    attempt = 1
    xpath = f'//span[text()[contains(., "{text}")]]'
    value = 0
    while attempt <= max_attempts:
        try:
            value = driver.find_element(By.XPATH, xpath).text
            break
        except:
            logger.error(f"Error getting value. Attempt {attempt} of {max_attempts}")
            time.sleep(2)
            attempt += 1
    return value


def get_rating(driver, company):
    logger.info(f"Getting rating for {company}")
    search = f"https://www.google.com/search?q={company}+glassdoor"
    driver.get(search)

    rating_msg = get_text(driver, "Rating")
    votes_msg = get_text(driver, "vote")

    if rating_msg:
        # We replace commas with dots in case the locale uses commas as
        # decimal separator (could be useful for local testing)
        rating = float(rating_msg.split(" ")[1].replace(",", "."))
    else:
        rating = 0

    if votes_msg:
        # We remove commas in case the value exceeds 1,000
        votes = int(votes_msg.split(" ")[0].replace(",", ""))
    else:
        votes = 0

    logger.info(f"Rating for {company}: {rating} with {votes} votes.")
    return [company, rating, votes]
