import uuid
from src.scraper import get_companies_in_page, get_company_info, click_next_page
from src.driver import get_driver
from utils.logging import logger
from utils.scraping.popups import handle_glassdoor_cookies_popup
import utils.data as data
import constants as const


driver = get_driver()

# Execution ID to identify the data uploaded to the bucket
execution_id = str(uuid.uuid4())[:8]
logger.info(f"Execution ID: {execution_id}")

logger.info("User agent: " + driver.execute_script("return navigator.userAgent;"))
current_page = const.STARTING_PAGE_NUMBER


driver.get(f"https://www.glassdoor.es/Opiniones/index.htm?overall_rating_low={const.MIN_RATING}&page={current_page}")
handle_glassdoor_cookies_popup(driver)


while True:
    logger.info(f"Scraping page {current_page}...")
    company_elements = get_companies_in_page(driver)
    companies = []
    for element in company_elements:
        companies.append(get_company_info(driver, element))

    logger.info(f"Page {current_page} scraped")
    data.write_csv(companies, const.CSV_PATH, const.CSV_HEADER, ";")

    if current_page % 30 == 0:
        data.upload_to_bucket(
            const.COMPANIES_BUCKET_NAME,
            "companies.csv",
            f"{execution_id}-{const.MIN_RATING}/companies-rating-{const.STARTING_PAGE_NUMBER}-{current_page}.csv",
            const.GCP_PROJECT
        )
        logger.info("Data uploaded to bucket")
    try:
        click_next_page(driver)
    except Exception as e:
        logger.error(e)
        break
    current_page += 1

driver.quit()

logger.info(f"Scraper finished. Data saved to {const.CSV_PATH}")
logger.info(f"Last page scraped: {current_page}")

# Upload the data to GCP. The data will be later sent to BigQuery using a Cloud Run job
data.upload_to_bucket(
    const.COMPANIES_BUCKET_NAME,
    "companies.csv",
    f"{execution_id}-{const.MIN_RATING}/companies-{const.STARTING_PAGE_NUMBER}-{current_page}.csv",
    const.GCP_PROJECT
)

logger.info("Scraping finished. Data uploaded to bucket.")
logger.info(f"Execution ID: {execution_id}")
