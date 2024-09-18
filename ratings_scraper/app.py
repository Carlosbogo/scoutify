
import time
import os

import program.helpers.popups as popups
from program.ratings import get_rating
import constants as const
import program.data as data
from program.driver import driver
from program.helpers.logging import logger


download_path = os.path.join(const.DOWNLOADS_FOLDER, "remote_in_spain.csv")
logger.info(f"Download path: {download_path}")

# Download and parse companies data, currently the only option is
# to download a existing CSV file stored in a Google Cloud Storage bucket
data.download_from_bucket(const.INPUT_BUCKET_NAME, "remote_in_spain.csv", download_path)
companies = data.parse("data/remote_in_spain.csv")

# Reject Google privacy popup if in local development
# (The popup is not present in the production environment)
if const.LOCAL_DEVELOPMENT:
    try:
        popups.reject_google_privacy_popup(driver, logger)
    except Exception as e:
        logger.error("Error rejecting Google privacy popup.")

# Get ratings for each company
ratings = []
for c in companies:
    time.sleep(5)
    try:
        ratings.append(get_rating(driver, c[0]) + [c[1]])
    except Exception as e:
        logger.error(f"Error getting rating for {c[0]}")
        logger.error(repr(e))
        # We continue with the next company in the case of an error
        continue

# Write ratings to CSV file and upload it to a Google Cloud Storage bucket
# In the near future we will have a Cloud Run job to forward the data to BigQuery
data.write_csv(ratings, "ratings.csv")
data.upload_to_bucket(const.RATINGS_BUCKET_NAME, "ratings.csv", "ratings.csv")
driver.quit()

logger.info("Ratings collected and uploaded to bucket.")
