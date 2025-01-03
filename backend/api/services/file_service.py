from django.db import transaction
from typing import Tuple, Dict, Optional
from datetime import datetime
import uuid
import logging

from ..models import FileUpload
from .s3 import S3Service
from ..exceptions import FileValidationError, StorageError
from .content_validator import ContentValidator
from ..constants.file_service_constants import FileValidationConstants, ContentValidationMessages
logger = logging.getLogger(__name__)

class FileService:
    def __init__(self):
        self.s3_service = S3Service()

    def _validate_content(self, content: str) -> None:
        """
        Validates file content for security concerns.
        """
        try:
            ContentValidator.validate_content(content)
        except FileValidationError as e:
            logger.warning(f"Content validation failed: {str(e)}")
            raise

    def _prepare_file_metadata(self, file_obj) -> Dict:
        """Prepares metadata for file upload."""
        return {
            'original_name': file_obj.name,
            'content_type': file_obj.content_type,
            'size': str(file_obj.size)
        }

    def _clean_s3_metadata(self, s3_metadata: Dict) -> Dict:
        """Cleans S3 metadata for storage."""
        return {
            'ETag': s3_metadata.get('ETag'),
            'VersionId': s3_metadata.get('VersionId'),
            'LastModified': s3_metadata.get('LastModified').isoformat() 
                          if s3_metadata.get('LastModified') else None,
            'content_type': s3_metadata.get('content_type'),
            'size': s3_metadata.get('size'),
            'original_name': s3_metadata.get('original_name')
        }

    def _validate_file(self, file_obj) -> None:
        """Validates file size, type and extension."""
        # Validate size
        if not (FileValidationConstants.MIN_SIZE_BYTES <= file_obj.size <= FileValidationConstants.MAX_SIZE_BYTES):
            raise FileValidationError(ContentValidationMessages.INVALID_SIZE)
        
        # Validate content type
        if file_obj.content_type != FileValidationConstants.ALLOWED_CONTENT_TYPE:
            raise FileValidationError(ContentValidationMessages.INVALID_TYPE)
        
        # Validate extension
        extension = file_obj.name.split('.')[-1].lower()
        if extension not in FileValidationConstants.ALLOWED_EXTENSIONS:
            raise FileValidationError(ContentValidationMessages.INVALID_EXTENSION)
        
        # Validate filename length
        if len(file_obj.name) > FileValidationConstants.MAX_FILENAME_LENGTH:
            raise FileValidationError(f"Filename exceeds {FileValidationConstants.MAX_FILENAME_LENGTH} characters")

    def _read_file_content(self, file_obj) -> str:
        """Reads and validates file content."""
        file_obj.seek(0)
        try:
            content = file_obj.read().decode('utf-8')
            file_obj.seek(0)
            return content
        except UnicodeDecodeError:
            raise FileValidationError("File must be UTF-8 encoded")

    def _read_and_validate_file_content(self, file_obj) -> str:
        """
        Reads and validates file content.
        """
        content = self._read_file_content(file_obj)
        self._validate_content(content)
        return content
    
    @transaction.atomic
    def create_file(self, file_obj) -> FileUpload:
        """
        Creates a file entry with atomic transaction support.
        Raises:
            FileValidationError: If file validation fails
            StorageError: If S3 storage operations fail
        """
        # Validate file
        self._validate_file(file_obj)
        content = self._read_and_validate_file_content(file_obj)

        # Prepare for S3 upload
        file_extension = file_obj.name.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        # Create a save point for transaction
        sid = transaction.savepoint()
        
        try:
            # Upload to S3
            s3_url, s3_metadata = self.s3_service.upload_file(
                file_obj,
                unique_filename,
                file_obj.content_type,
                self._prepare_file_metadata(file_obj)
            )

            if not s3_url:
                raise StorageError("Failed to upload file to S3")

            # Create database record
            file_upload = FileUpload.objects.create(
                name=file_obj.name,
                size=file_obj.size / 1024,  # Convert to KB
                content=content,
                s3_url=s3_url,
                file_type=file_obj.content_type,
                s3_etag=s3_metadata.get('ETag'),
                s3_version_id=s3_metadata.get('VersionId'),
                s3_metadata=self._clean_s3_metadata(s3_metadata)
            )

            # If everything succeeded, commit the transaction
            transaction.savepoint_commit(sid)
            return file_upload

        except Exception as e:
            # If anything fails, rollback the transaction and try to clean up S3
            transaction.savepoint_rollback(sid)
            try:
                self.s3_service.delete_file(unique_filename)
            except Exception as cleanup_error:
                logger.error(f"Failed to cleanup S3 file after transaction failure: {cleanup_error}")
            raise

    @transaction.atomic
    def delete_file(self, file_upload: FileUpload) -> None:
        """
        Deletes a file with atomic transaction support.
        """
        if file_upload.s3_url:
            file_name = file_upload.s3_url.split('/')[-1]
            if not self.s3_service.delete_file(file_name):
                raise StorageError("Failed to delete file from S3")

        file_upload.delete()