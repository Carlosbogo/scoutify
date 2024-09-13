
import time
import os

import program.helpers.popups as popups
from program.ratings import get_rating
import constants as const
import program.data as data
from program.driver import driver
from program.helpers.logging import logger


ratings = {}
download_path = os.path.join(const.DOWNLOADS_FOLDER, "remote_in_spain.csv")
logger.info(f"Download path: {download_path}")


data.download_from_bucket(const.INPUT_BUCKET_NAME, "remote_in_spain.csv", download_path)
companies = data.parse("data/remote_in_spain.csv")


if const.LOCAL_DEVELOPMENT:
    try:
        popups.reject_google_privacy_popup(driver, logger)
        logger.info("Google privacy popup rejected.")
    except Exception as e:
        logger.error("Error rejecting Google privacy popup.")


for c in companies:
    time.sleep(5)
    try:
        ratings.update(get_rating(driver, c[0]))
    except Exception as e:
        logger.error(f"Error getting rating for {c[0]}")
        logger.error(repr(e))
        continue

data.write_csv(
    [[k, v] for k, v in ratings.items()], "ratings.csv"
)
data.upload_to_bucket(const.RATINGS_BUCKET_NAME, "ratings.csv", "ratings.csv")
driver.quit()

logger.info("Ratings collected and uploaded to bucket.")
