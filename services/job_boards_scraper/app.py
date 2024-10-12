import time
import random

from src.job_boards import get_job_board
import constants as const
import utils.data as data
from src.driver import get_driver
from utils.logging import logger

driver = get_driver()

# Download and parse companies data, currently the only option is
# to download a existing CSV file stored in a Google Cloud Storage bucket

input_file = data.download_from_bucket(const.INPUT_BUCKET_NAME, const.INPUT_FILE, const.INPUT_FILE, const.GCP_PROJECT)
logger.info(f"Downloaded file {input_file}")
companies = data.parse(input_file, delimiter=";")
# companies = [["Bending Spoons"], ["Spotify"], ["TomTom"]]

# Get the job board for each company

for company in companies:
    time.sleep(random.randint(1, 3))
    try:
        company.append(get_job_board(driver, company[0]))
    except Exception as e:
        logger.error(f"Error getting job board for {company[0]}")
        logger.error(repr(e))
        company.append(None)
        # We continue with the next company in the case of an error
        continue

# Write ratings to CSV file and upload it to a Google Cloud Storage bucket
# In the near future we will have a Cloud Run job to forward the data to BigQuery
data.write_csv(companies, const.OUTPUT_FILE, ";")
data.upload_to_bucket(const.OUTPUT_BUCKET_NAME, const.OUTPUT_FILE, const.OUTPUT_FILE, const.GCP_PROJECT)
driver.quit()

logger.info("Job boards collected and uploaded to bucket.")
