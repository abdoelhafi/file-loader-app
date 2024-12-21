from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock
from api.models import FileUpload
from .test_constants import TEST_FILES, S3_CONFIG
import json

class FileUploadViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_file = TEST_FILES['VALID_TEXT']
        self.s3_config = S3_CONFIG
        
        # Create test file for upload
        self.upload_file = SimpleUploadedFile(
            self.test_file['name'],
            self.test_file['content'].encode(),
            content_type=self.test_file['type']
        )

        # Mock S3 response data
        self.s3_response = {
            'ETag': self.s3_config['TEST_ETAG'],
            'VersionId': self.s3_config['TEST_VERSION'],
            'LastModified': '2024-12-20T00:00:00Z'
        }

        # API endpoints
        self.list_url = '/api/files/'
        self.upload_url = '/api/files/'

    @patch('api.services.s3.S3Service')
    def test_file_upload(self, mock_s3_service):
        """Test file upload with mocked S3 service"""
        mock_s3_instance = mock_s3_service.return_value
        mock_s3_instance.upload_file.return_value = (
            f"{self.s3_config['BUCKET_URL']}/{self.test_file['name']}",
            self.s3_response
        )

        response = self.client.post(
            self.upload_url,
            {'file': self.upload_file},
            format='multipart'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FileUpload.objects.count(), 1)
        self.assertEqual(response.data['data']['name'], self.test_file['name'])

    def test_file_upload_no_file(self):
        """Test file upload without file"""
        response = self.client.post(self.upload_url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('api.services.s3.S3Service')
    def test_file_deletion(self, mock_s3_service):
        """Test file deletion with mocked S3 service"""
        # Create test file
        file = FileUpload.objects.create(
            name=self.test_file['name'],
            size=self.test_file['size'],
            content=self.test_file['content'],
            file_type=self.test_file['type'],
            s3_url=f"{self.s3_config['BUCKET_URL']}/{self.test_file['name']}"
        )

        mock_s3_instance = mock_s3_service.return_value
        mock_s3_instance.delete_file.return_value = True

        response = self.client.delete(f'{self.upload_url}{file.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FileUpload.objects.count(), 0)