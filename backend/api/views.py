# api/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from datetime import datetime
import uuid
import logging

from .models import FileUpload
from .serializers import FileUploadSerializer
from .services.s3 import S3Service
from .utils.response import create_api_response

logger = logging.getLogger(__name__)

class FileUploadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling file uploads, storage, and management.
    Supports create, list, retrieve, and delete operations.
    """
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3_service = S3Service()

    def _prepare_file_metadata(self, file_obj):
        """
        Prepares metadata for file upload.
        """
        return {
            'original_name': file_obj.name,
            'content_type': file_obj.content_type,
            'size': str(file_obj.size)
        }

    def _clean_s3_metadata(self, s3_metadata):
        """
        Cleans S3 metadata for storage.
        """
        return {
            'ETag': s3_metadata.get('ETag'),
            'VersionId': s3_metadata.get('VersionId'),
            'LastModified': s3_metadata.get('LastModified').isoformat() 
                          if s3_metadata.get('LastModified') else None,
            'content_type': s3_metadata.get('content_type'),
            'size': s3_metadata.get('size'),
            'original_name': s3_metadata.get('original_name')
        }

    def create(self, request, *args, **kwargs):
        """
        Handles file upload: reads file, uploads to S3, and stores metadata.
        """
        try:
            # Validate file presence
            if 'file' not in request.FILES:
                return create_api_response(
                    error="No file provided",
                    status=status.HTTP_400_BAD_REQUEST
                )

            file_obj = request.FILES['file']
            
            # Read file content
            file_obj.seek(0)
            try:
                content = file_obj.read().decode('utf-8')
            except UnicodeDecodeError:
                return create_api_response(
                    error="File must be text-based",
                    status=status.HTTP_400_BAD_REQUEST
                )
            file_obj.seek(0)
            
            # Generate unique filename
            file_extension = file_obj.name.split('.')[-1]
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            
            # Upload to S3
            s3_url, s3_metadata = self.s3_service.upload_file(
                file_obj,
                unique_filename,
                file_obj.content_type,
                self._prepare_file_metadata(file_obj)
            )
            
            if not s3_url:
                return create_api_response(
                    error="Failed to upload file to S3",
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Prepare file data for database
            file_data = {
                'name': file_obj.name,
                'size': file_obj.size / 1024,  # Convert to KB
                'content': content,
                's3_url': s3_url,
                'file_type': file_obj.content_type,
                's3_etag': s3_metadata.get('ETag'),
                's3_version_id': s3_metadata.get('VersionId'),
                's3_metadata': self._clean_s3_metadata(s3_metadata)
            }

            # Validate and save
            serializer = self.get_serializer(data=file_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return create_api_response(
                data=serializer.data,
                message="File uploaded successfully",
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            logger.error(f"File upload error: {str(e)}")
            return create_api_response(
                error=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        """
        Lists all files with optimized response (excludes file content).
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            
            # Optimize response by excluding content
            data = serializer.data
            for file_data in data:
                file_data.pop('content', None)
            
            return create_api_response(
                data=data,
                message="Files retrieved successfully"
            )
        except Exception as e:
            logger.error(f"File list error: {str(e)}")
            return create_api_response(
                error=f"Error occured while listing files: {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        """
        Deletes file from both S3 and database.
        """
        try:
            instance = self.get_object()
            
            # Handle case where file exists only in database
            if not instance.s3_url:
                self.perform_destroy(instance)
                return create_api_response(
                    message="Database record deleted successfully",
                    status=status.HTTP_204_NO_CONTENT
                )

            # Delete from S3 and database
            file_name = instance.s3_url.split('/')[-1]
            if self.s3_service.delete_file(file_name):
                self.perform_destroy(instance)
                return create_api_response(
                    message="File deleted successfully",
                    status=status.HTTP_204_NO_CONTENT
                )
            
            return create_api_response(
                error="Failed to delete file from S3",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            logger.error(f"File deletion error: {str(e)}")
            return create_api_response(
                error=f"Error occured while deleting File: {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )