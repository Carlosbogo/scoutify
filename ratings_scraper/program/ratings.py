import time
import os
from selenium.webdriver.common.by import By
from program.helpers.logging import logger


def get_text(driver, text, max_attempts=5):
    """
    Gets the contents of an element that contains the given text.

    Args:
        driver: Selenium WebDriver
        text: Text to search for
        max_attempts: Maximum number of attempts to get the text

    Returns:
        str: Text of the element
    """
    attempt = 1
    xpath = f'//span[text()[contains(., "{text}")]]'
    value = 0

    # We try to get the text of the element up to max_attempts times
    # to avoid errors due to the element not being loaded yet
    while attempt <= max_attempts:
        try:
            value = driver.find_element(By.XPATH, xpath).text
            # If we get the value, we break the loop
            break
        except:
            logger.error(f"Error getting value. Attempt {attempt} of {max_attempts}")
            # We set a wait time between attempts to allow the element to load
            # and to avoid overloading the server
            time.sleep(2)
            attempt += 1
    return value


def get_rating(driver, company):
    """
    Gets the Glassdoor rating and number of votes for a company
    using Google search results.

    Args:
        driver: Selenium WebDriver
        company: Name of the company

    Returns:
        list: [Company name, rating, number of votes]
    """
    logger.info(f"Getting rating for {company}")

    # We search for the company on Google and add "glassdoor" to the query
    search = f"https://www.google.com/search?q={'+'.join(company.split())}+glassdoor"
    driver.get(search)

    # We get the rating and number of votes from the search results
    rating_msg = get_text(driver, "Rating")
    votes_msg = get_text(driver, "vote")

    if rating_msg:
        # We replace commas with dots in case the locale uses commas as
        # decimal separator (could be useful for local testing)
        rating = float(rating_msg.split(" ")[1].replace(",", "."))
    else:
        rating = 0

    if votes_msg:
        # We remove commas and dots in case the value exceeds 1,000
        # (taking dots into account could be useful for local testing)
        votes = int(votes_msg.split(" ")[0].replace(",", ""). replace(".", ""))
    else:
        votes = 0

    logger.info(f"Rating for {company}: {rating} with {votes} votes.")
    # Defult values for rating and votes are both 0
    return [company, rating, votes]
