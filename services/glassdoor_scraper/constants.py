import os
import dotenv

dotenv.load_dotenv(".env")

GCP_PROJECT = os.getenv("GCP_PROJECT")
COMPANIES_BUCKET_NAME = os.getenv("COMPANIES_BUCKET_NAME")

STARTING_PAGE_NUMBER = int(os.getenv("STARTING_PAGE_NUMBER", 1))
MIN_RATING = os.getenv("MIN_RATING", 3.5)

CSV_PATH = os.getenv("CSV_PATH", "companies.csv")
CSV_HEADER = ["Company", "Rating", "Reviews", "Locations"]