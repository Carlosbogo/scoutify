import csv
import os
import google.cloud.storage
from utils.logging import logger
from typing import List, Optional


def download_from_bucket(
    bucket_name: str, source_blob_name: str, destination_file_name: str, gcp_project: str
) -> None:
    """
    Downloads a blob from the specified bucket.
    Params:
    - bucket_name: the name of the bucket.
    - source_blob_name: the name of the blob to download.
    - destination_file_name: the name of the file to save the blob.

    Returns:
    - None
    """
    storage_client = google.cloud.storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    logger.info(f"Downloading blob {source_blob_name}.")

    try:
        blob.download_to_filename(destination_file_name)
    except Exception as e:
        logger.error(f"Error downloading blob {source_blob_name}: {e}")

    logger.info(f"Blob {source_blob_name} downloaded to {destination_file_name}.")


def parse(filepath: str, delimiter: str = ",") -> List[List[str]]:
    """
    Parse a CSV file into a list of lists.
    Params:
    - filepath: str - the path of the file to parse.
    - delimiter: str - the delimiter used in the file.

    Returns:
    - List[List[str]]: The parsed data as a list of lists.
    """
    try:
        with open(filepath, newline="", encoding="utf8") as f:
            reader = csv.reader(f, delimiter=delimiter)
            data = list(reader)
    except FileNotFoundError as e:
        logger.error(f"File {filepath} not found.")
        data = []
    except Exception as e:
        logger.error(f"Error parsing file {filepath}: {e}")
        data = []
    return data


def create_csv(filepath: str, header: Optional[List[str]], delimiter: str = ",") -> None:
    """
    Create a CSV file with a header.
    Params:
    - filepath: str - the path of the file to create.
    - header: List[str] - the header of the file.
    - delimiter: str - the delimiter to use in the file.

    Returns:
    - None
    """
    with open(filepath, "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f, delimiter=delimiter)
        if header:
            writer.writerow(header)


def write_csv(data: List[List[str]], filepath: str, header: Optional[List[str]], delimiter: str = ",") -> None:
    """
    Write a list of lists to a CSV file.
    Params:
    - data: List[List[str]] - the data to write to the file.
    - header: List[str] - the header of the file.
    - filepath: str - the path of the file to write.
    - delimiter: str - the delimiter to use in the file.

    Returns:
    - None
    """
    if not os.path.exists(filepath):
        create_csv(filepath, header, delimiter)

    with open(filepath, "a", newline="", encoding="utf8") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(data)


def upload_to_bucket(
    bucket_name: str, source_file_path: str, destination_blob_name: str, gcp_project: str,
) -> None:
    """
    Uploads a file to a GCP storage bucket.
    Params:
    - bucket_name: str - the name of the bucket.
    - source_file_path: str - the path of the file to upload.
    - destination_blob_name: str - the name of the blob to create.

    Returns:
    - None
    """
    storage_client = google.cloud.storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    logger.info(f"Uploading {source_file_path} to {destination_blob_name}.")
    try:
        blob.upload_from_filename(source_file_path)
    except Exception as e:
        logger.error(f"Error uploading {source_file_path}: {e}")

    logger.info(f"File {source_file_path} uploaded to {destination_blob_name}.")
