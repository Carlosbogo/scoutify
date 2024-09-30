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


    def get_company_data(self, company_name):
        search_url = f"{self.base_url}/Reviews/{company_name}-reviews-SRCH_KE0,{len(company_name)}.htm"
        self.driver.get(search_url)
        time.sleep(2)  # Wait for the page to load


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


    def get_all_companies(self, max_pages=15):
        companies_data = []
        for page in range(1, max_pages + 1):
            search_url = f"{self.base_url}/Reviews/company-reviews-SRCH_IL.0,0_IN0_IP{page}.htm"
            self.driver.get(search_url)
            time.sleep(2)  # Wait for the page to load


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
