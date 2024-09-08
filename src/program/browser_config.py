from selenium.webdriver.chrome.options import Options

config = Options()

language = "en"

config.add_argument(f"--lang={language}")
config.add_argument("--disable-search-engine-choice-screen")
config.add_argument("--headless=new")
