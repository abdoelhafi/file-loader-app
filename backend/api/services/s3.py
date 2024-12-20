import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import logging
import mimetypes

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    def upload_file(self, file_obj, file_name, content_type=None, metadata=None):
        """
        Upload a file to S3 with metadata
        Returns: (S3 URL, metadata) tuple if successful, (None, None) if failed
        """
        try:
            extra_args = {
                'ContentType': content_type or mimetypes.guess_type(file_name)[0],
                'ACL': 'private',
                'Metadata': metadata or {}
            }
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                file_name,
                ExtraArgs=extra_args
            )

            # Get object metadata after upload
            response = self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            logger.info(f"------------tyring to save file got response {response}")

            s3_metadata = {
                'ETag': response.get('ETag', '').strip('"'),
                'VersionId': response.get('VersionId'),
                'LastModified': response.get('LastModified'),
                **response.get('Metadata', {})
            }

            # Generate the URL
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
            return url, s3_metadata

        except ClientError as e:
            logger.error(f"Error uploading file to S3: {str(e)}")
            return None, None

    def delete_file(self, file_name):
        """Delete a file from S3"""
        logger.info(f"trying to delete file  : {file_name}")
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_name
            )
            return True
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {str(e)}")
         