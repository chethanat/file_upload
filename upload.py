import os
import logging
import boto3
from google.cloud import storage
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileLoader:
    def __init__(self, s3_bucket_name = Config.DEFAULT_S3_BUCKET_NAME,
                 gcs_bucket_name = Config.DEFAULT_GCS_BUCKET_NAME,
                 s3_file_types = Config.DEFAULT_S3_FILE_TYPES,
                 gcs_file_types = Config.DEFAULT_GCS_FILE_TYPES):
        """
        Initialize FileLoader
        Args:
            s3_bucket_name: The name of S3 bucket.
            gcs_bucket_name: The name of Google Cloud Storage bucket
            s3_file_types: List of file extensions to be uploaded to S3
            gcs_file_types: List of file extensions to be uploaded to GCS
        """
        self.s3_client = self.create_s3_client()
        self.s3_bucket_name = s3_bucket_name
        self.gcs_client = self.create_gcs_client()
        self.gcs_bucket = self.retrive_gcs_bucket(gcs_bucket_name)
        self.s3_file_types = s3_file_types
        self.gcs_file_types = gcs_file_types

    def create_s3_client(self):
        """
        To create and return AWS S3 Client
        :return: s3 client
        """
        try:
            s3_client = boto3.client('s3')
            logger.info("Connected to AWS S3")
            return s3_client
        except Exception as e:
            logger.error(f"Failed to connect to AWS s3: {str(e)}")
            raise


    def create_gcs_client(self):
        """
        To create and return a Google Cloud Storage Client
        :return: gcs client
        """
        try:
            gcs_client = storage.Client()
            logger.info("Connected to Google Coud Storage")
            return gcs_client
        except Exception as e:
            logger.error(f"Failed to connect to Google Cloud Storage")
            raise

    def retrive_gcs_bucket(self, bucket_name):
        """
        To retrive gcs bucket
        :param bucket_name: gcs bucket name
        :return: gcs bucket
        """
        try:
            bucket = self.gcs_client.get_bucket(bucket_name)
            logger.info(f"Retrived Google Coud Storage bucket: {bucket_name}")
            return bucket
        except Exception as e:
            logger.error(f"Failed to retrive GCS bucket: {str(e)}")
            raise

    def upload_to_s3(self, file_path):
        """
        Upload file to AWS S3
        :param file_path: The path of file to upload
        """
        try:
            file_name = os.path.basename(file_path)
            self.s3_client.upload_file(file_path, self.s3_bucket_name, file_name)
            logger.info(f"Uploaded {file_name} to s3 bucket")
        except Exception as e:
            logger.error(f"Failed to upload file to s3: {str(e)}")
            raise

    def upload_to_gcs(self, file_path):
        """
        Upload file to gcs
        :param file_path: The path of file to upload
        """
        try:
            file_name = os.path.basename(file_path)
            blob = self.gcs_bucket.blob(file_name)
            blob.upload_from_filename(file_path)
            logger.info(f"Uploaded {file_name} to GCS bucket")
        except Exception as e:
            logger.error(f"Failed to upload file to GCS: {str(e)}")
            raise

    def upload_files(self, directory):
        """
        Upload files from specific directory to AWS S3 and GCS
        :param directory: The directory to scan for files
        """
        try:
            for root, _, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_extension = file.split('.')[-1].lower()
                    if file_extension in self.s3_file_types:
                        self.upload_to_s3(file_path)
                    elif file_extension in self.gcs_file_types:
                        self.upload_to_gcs(file_path)
                    else:
                        logger.error(f"Unsupported file type {file_extension}")
                        raise
        except Exception as error:
            logger.error(f"Exception in upload_files function: {str(e)}")
            raise
