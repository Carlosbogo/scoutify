from selenium.webdriver.common.by import By

def get_rating(driver, company):
    search = f"https://www.google.com/search?q={company}+glassdoor"
    driver.get(search)
    driver.implicitly_wait(10)
    rating_msg = driver.find_element(By.XPATH, '//span[text()[contains(.,"Valoración")]]').text
    rating = float(rating_msg.split(" ")[1].replace(",", "."))
    return {company: rating}
