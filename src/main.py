"""Download file and upload to AWS"""

from sys import stderr

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


def download_file(url, path):
    """Download file from URL"""
    import requests

    response = requests.get(url)
    with open(path, "wb") as file:
        file.write(response.content)

    return path


def upload_file(file_path, bucket_name, aws_access_key_id, aws_secret_access_key):
    """Upload file to AWS S3 bucket"""
    project = "big_data_ada/"
    file_name = project + file_path.split("/")[-1]
    s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    s3.upload_file(file_path, bucket_name, file_name)


if __name__ == "__main__":
    logger.info("Starting download and upload process")

    logger.info("Reading configuration")
    config = dotenv_values(".env")

    bucket_name = config["BUCKET_NAME"]
    aws_access_key_id = config["AWS_ACCESS_KEY_ID"]
    aws_secret_access_key = config["AWS_SECRET_ACCESS_KEY"]
    logger.info("Configuration read successfully")

    logger.info("Downloading file")

    path = download_file(
        "https://dados.agricultura.gov.br/dataset/58bdc09c-9778-42b9-8fce-7d5c2c4fa211/resource/daf8053b-5446-4cd4-986a-f141b4a434ec/download/temas_ambientais.csv",
        "../data/temas_ambientais.csv",
    )

    logger.info("File downloaded successfully")

    logger.info("Uploading file")

    upload_file(path, bucket_name, aws_access_key_id, aws_secret_access_key)

    logger.info("File uploaded successfully")

    logger.info("Process finished")
