from selenium.webdriver.chrome.options import Options

config = Options()

language = "en-US"

config.add_argument(f"--lang={language}")
config.add_argument("--disable-search-engine-choice-screen")
config.add_argument("--headless=new")
config.add_argument("-width=1920")
config.add_argument("-height=1080")
config.add_argument("--no-sandbox")
config.add_argument("--disable-gpu")