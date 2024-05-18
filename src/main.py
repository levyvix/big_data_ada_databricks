"""Download file and upload to AWS"""

from sys import stderr
from typing import Tuple

import boto3
from dotenv import dotenv_values
from loguru import logger

logger.remove()
logger.add(
    "logs/main.log",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <r>{level}</r> <g>{message}</g> {file}",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
)

logger.add(
    sink=stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> <r>{level}</r> <g>{message}</g> {file}",
    level="INFO",
)


def download_file(url: str, file_path: str) -> Tuple[str, int]:
    """
    Download file from URL.

    Args:
        url (str): The URL of the file to download.
        file_path (str): The path to save the downloaded file.

    Returns:
        str: The file path of the downloaded file.
        int: The HTTP status code of the response.
    """
    import requests

    # Send a GET request to the URL and stream the response
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Open the file in binary mode and write the response chunks to the file
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    # Return the file path of the downloaded file and the HTTP status code
    return file_path, response.status_code


def upload_file(
    file_path: str, bucket_name: str, aws_access_key_id: str, aws_secret_access_key: str
) -> None:
    """
    Upload file to AWS S3 bucket.

    Args:
        file_path (str): Path to the file to upload.
        bucket_name (str): Name of the S3 bucket to upload to.
        aws_access_key_id (str): AWS access key ID.
        aws_secret_access_key (str): AWS secret access key.

    Returns:
        None
    """
    # Extract file name from the file path
    file_name = "big_data_ada/" + file_path.split("/")[-1]

    # Create an S3 client with high-level transfer configuration
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    # Upload the file to the S3 bucket
    s3_client.upload_file(file_path, bucket_name, file_name)


def main():
    logger.info("Starting download and upload process")

    logger.info("Reading configuration")
    config = dotenv_values(".env")

    bucket_name = config["BUCKET_NAME"]
    aws_access_key_id = config["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = config["AWS_SECRET_ACCESS_KEY"]
    logger.info("Configuration read successfully")

    logger.info("Downloading file")

    path, status_code = download_file(
        "https://dados.agricultura.gov.br/dataset/58bdc09c-9778-42b9-8fce-7d5c2c4fa211/resource/daf8053b-5446-4cd4-986a-f141b4a434ec/download/temas_ambientais.csv",
        "../data/temas_ambientais.csv",
    )

    logger.info(f"File downloaded successfully. HTTP status code: {status_code}")

    logger.info("Uploading file")

    upload_file(path, bucket_name, aws_access_key_id, aws_secret_access_key)

    logger.info("File uploaded successfully")

    logger.info("Process finished")


if __name__ == "__main__":
    main()
