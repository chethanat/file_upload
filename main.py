import logging
from upload import FileLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    directory = '/path-to-directory'
    s3_bucket_name = 'your-s3-bucket'
    gcs_bucket_name = 'your-gcs-bucket'
    try:
        uploader = FileLoader(s3_bucket_name=s3_bucket_name, gcs_bucket_name=gcs_bucket_name)

        #start the upload process
        logger.info("Start uploading the files")
        uploader.upload_files(directory)
    except Exception as e:
        logger.error(f"Error occured in main function and error is: {str(e)}")
        raise