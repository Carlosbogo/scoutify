import os
import dotenv

dotenv.load_dotenv(".env")

GCP_PROJECT = os.getenv("GCP_PROJECT")
INPUT_BUCKET_NAME = os.getenv("INPUT_BUCKET_NAME")
RATINGS_BUCKET_NAME = os.getenv("RATINGS_BUCKET_NAME")
DOWNLOADS_FOLDER = os.getenv("DOWNLOADS_FOLDER")
LOCAL_DEVELOPMENT = os.getenv("LOCAL_DEVELOPMENT")
