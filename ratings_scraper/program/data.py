import csv
import google.cloud.storage
import constants as const
from program.helpers.logging import logger
from typing import List


def download_from_bucket(
    bucket_name: str, source_blob_name: str, destination_file_name: str
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
    storage_client = google.cloud.storage.Client(project=const.GCP_PROJECT)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    logger.info(f"Downloading blob {source_blob_name}.")

    blob.download_to_filename(destination_file_name)

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
    with open(filepath, newline="", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=delimiter)
        data = list(reader)
    return data


def write_csv(data: List[List[str]], filepath: str, delimiter: str = ",") -> None:
    """
    Write a list of lists to a CSV file.
    Params:
    - data: List[List[str]] - the data to write to the file.
    - filepath: str - the path of the file to write.
    - delimiter: str - the delimiter to use in the file.

    Returns:
    - None
    """
    with open(filepath, "w", newline="", encoding="utf8") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerows(data)


def upload_to_bucket(
    bucket_name: str, source_file_path: str, destination_blob_name: str
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
    storage_client = google.cloud.storage.Client(project=const.GCP_PROJECT)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    logger.info(f"Uploading {source_file_path} to {destination_blob_name}.")

    blob.upload_from_filename(source_file_path)

    logger.info(f"File {source_file_path} uploaded to {destination_blob_name}.")
