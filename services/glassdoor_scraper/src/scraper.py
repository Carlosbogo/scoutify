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


        # Example: Extract company rating
        try:
            rating_element = self.driver.find_element(By.CLASS_NAME, 'rating')
            company_data['rating'] = rating_element.text.strip()
        except:
            company_data['rating'] = None

        # Example: Extract number of reviews
        try:
            reviews_element = self.driver.find_element(By.CLASS_NAME, 'reviews')
            company_data['reviews'] = reviews_element.text.strip()
        except:
            company_data['reviews'] = None


def get_company_info(driver: Driver, company: WebElement, get_locations: bool = False):
    time.sleep(random.uniform(0.1, 0.3))
    company_name = company.find_element(By.XPATH, ".//h2[@data-test='employer-short-name']").text
    company_rating = company.find_element(By.XPATH, ".//span[@data-test='rating']").text.replace(",", ".")
    review_string = company.find_element(By.XPATH, ".//h3[@data-test='cell-Reviews-count']").text
    review_count = format_reviews_string(review_string)
    if get_locations:
        locations = get_company_locations(driver, company)
    logger.info(f"Company: {company_name} - Rating: {company_rating} - Reviews: {review_count}")
    return [company_name, company_rating, review_count]


            for company_element in company_elements:
                try:
                    company_name_element = company_element.find_element(By.CLASS_NAME, 'company-tile-name')
                    company_name = company_name_element.text.strip()
                    print(f"Getting data for {company_name}")
                    company_data = self.get_company_data(company_name)
                    if company_data:
                        companies_data.append({company_name: company_data})
                except:
                    continue

            time.sleep(1)  # Be polite and don't hammer the server

        return companies_data

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    scraper = GlassdoorScraperSelenium(base_url="https://www.glassdoor.com")
    all_companies_data = scraper.get_all_companies()
    for company in all_companies_data:
        print(company)
    scraper.close()
