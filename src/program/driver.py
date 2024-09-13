from selenium import webdriver
from program.browser_config import config

driver = webdriver.Chrome(options=config)
driver.implicitly_wait(5)
driver.get("https://www.google.com")
companies = ["google", "apple"]