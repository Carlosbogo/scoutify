from selenium import webdriver
from src.browser_config import config

driver = webdriver.Chrome(options=config)
driver.implicitly_wait(10)
driver.get("https://www.google.com")
