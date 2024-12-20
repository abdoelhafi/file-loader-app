from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import FileUpload
from .serializers import FileUploadSerializer
from .services.s3 import S3Service
import uuid

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.s3_service = S3Service()

    def create(self, request, *args, **kwargs):
        try:
            file_obj = request.FILES['file']
            
            # Read file
            file_obj.seek(0)  # Ensure we're at the start of the file
            content = file_obj.read().decode('utf-8')
            file_obj.seek(0)  # Reset file pointer for S3 upload
            
            # Generate filename
            file_extension = file_obj.name.split('.')[-1]
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            
            # Prepare metadata
            metadata = {
                'original_name': file_obj.name,
                'content_type': file_obj.content_type,
                'size': str(file_obj.size)
            }
            
            # Upload to S3
            s3_url, s3_metadata = self.s3_service.upload_file(
                file_obj,
                unique_filename,
                file_obj.content_type,
                metadata
            )
            
            cleaned_metadata = {
                'ETag': s3_metadata.get('ETag'),
                'VersionId': s3_metadata.get('VersionId'),
                'LastModified': s3_metadata.get('LastModified').isoformat() if s3_metadata.get('LastModified') else None,  # Convert datetime to string
                'content_type': s3_metadata.get('content_type'),
                'size': s3_metadata.get('size'),
                'original_name': s3_metadata.get('original_name')
            }

            print(f"s3_url: {s3_url} and s3_metadata  : {s3_metadata}")
            if not s3_url:
                return Response(
                    {'error': 'Failed to upload file to S3'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Create file data
            file_data = {
                'name': file_obj.name,
                'size': file_obj.size / 1024,  # Convert to KB
                'content': content,
                's3_url': s3_url,
                'file_type': file_obj.content_type,
                's3_etag': s3_metadata.get('ETag'),
                's3_version_id': s3_metadata.get('VersionId'),
                's3_metadata': cleaned_metadata  # Use the cleaned metadata
            }

            serializer = self.get_serializer(data=file_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        # Exclude content field from list view for better performance
        for file_data in serializer.data:
            file_data.pop('content', None)
        
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.__dict__)
        # Extract filename from S3 URL
        file_name = instance.s3_url.split('/')[-1]
        print(f"file_name is ------------------------------------------: {file_name} and instance is {instance}")
        # Delete from S3
        if self.s3_service.delete_file(file_name):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response(
            {'error': 'Failed to delete file from S3'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )