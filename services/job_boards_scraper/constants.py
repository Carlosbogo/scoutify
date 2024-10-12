import os
import dotenv

dotenv.load_dotenv(".env")

GCP_PROJECT = os.getenv("GCP_PROJECT")
INPUT_BUCKET_NAME = os.getenv("INPUT_BUCKET_NAME")
OUTPUT_BUCKET_NAME = os.getenv("OUTPUT_BUCKET_NAME")
DOWNLOADS_FOLDER = os.getenv("DOWNLOADS_FOLDER")
INPUT_FILE = os.getenv("INPUT_FILE")
OUTPUT_FILE = os.getenv("OUTPUT_FILE")
LOCAL_DEVELOPMENT = os.getenv("LOCAL_DEVELOPMENT")
