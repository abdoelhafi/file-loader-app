# api/views.py
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
import logging

from .models import FileUpload
from .serializers import FileUploadSerializer
from .services.file_service import FileService
from .exceptions import FileValidationError, StorageError
from .utils.response import create_api_response

logger = logging.getLogger(__name__)

class FileUploadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling file uploads, storage, and management.
    """
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file_service = FileService()

    def create(self, request, *args, **kwargs):
        """Handle file upload"""
        try:
            if 'file' not in request.FILES:
                return create_api_response(
                    error="No file provided",
                    status=status.HTTP_400_BAD_REQUEST
                )

            file_upload = self.file_service.create_file(request.FILES['file'])
            serializer = self.get_serializer(file_upload)
            
            return create_api_response(
                data=serializer.data,
                message="File uploaded successfully",
                status=status.HTTP_201_CREATED
            )

        except FileValidationError as e:
            return create_api_response(
                error=str(e),
                status=status.HTTP_400_BAD_REQUEST
            )
        except StorageError as e:
            return create_api_response(
                error=str(e),
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.error(f"Unexpected error during file upload: {str(e)}")
            return create_api_response(
                error="An unexpected error occurred",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request, *args, **kwargs):
        """List all files"""
        try:
            queryset = self.get_queryset().defer('content')
            serializer = self.get_serializer(queryset, many=True)
            return create_api_response(
                data=serializer.data,
                message="Files retrieved successfully"
            )
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return create_api_response(
                error="Failed to retrieve files",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        """Delete file"""
        try:
            instance = self.get_object()
            self.file_service.delete_file(instance)
            return create_api_response(
                message="File deleted successfully",
                status=status.HTTP_204_NO_CONTENT
            )
        except StorageError as e:
            return create_api_response(
                error=str(e),
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return create_api_response(
                error="Failed to delete file",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )