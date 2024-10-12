from utils.logging import logger
from seleniumbase import Driver


def get_job_board(driver: Driver, company: str) -> str:
    """
    Gets the jobs board of a company by searching for it on Google.

    Args:
        driver: Selenium WebDriver
        company: Name of the company

    Returns:
        str: url of the job board
    """
    logger.info(f"Getting job board for {company}")

    # We search for the company on Google and add "jobs" to the query
    search = f"https://www.google.com/search?q={'+'.join(company.split())}+jobs"
    driver.get(search)

    # We wait for the search results to load and get the first
    driver.wait_for_element("h3")
    job_board = driver.get_attribute('div#search a', 'href')
    logger.info(f"Job board for {company}: {job_board}")

    return job_board
