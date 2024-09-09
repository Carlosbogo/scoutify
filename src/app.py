
import time
import os

import program.helpers.popups as popups
from program.ratings import get_rating
from data.parse_data import parse
from program.driver import driver
from program.helpers.logging import logger


ratings = {}
companies = parse(os.path.join(os.getcwd(), "data\\remote_companies.csv"))


try:
    popups.reject_google_privacy_popup(driver, logger)
    driver.implicitly_wait(10)
    for c in companies:
        ratings.update(get_rating(driver, c[0]))
    
except Exception as e:
    print(repr(e))
    print(e)
    time.sleep(2)

finally:
    driver.quit()

print("finished")
