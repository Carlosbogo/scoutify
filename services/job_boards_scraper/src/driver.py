from seleniumbase import Driver


def get_driver() -> Driver:
    driver = Driver(browser="chrome", uc=True, incognito=True, headless=True)
    driver.implicitly_wait(10)
    return driver

