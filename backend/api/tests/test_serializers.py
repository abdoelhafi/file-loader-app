from django.test import TestCase
from api.serializers import FileUploadSerializer
from .test_constants import TEST_FILES, S3_CONFIG

class FileUploadSerializerTest(TestCase):
    def setUp(self):
        self.test_file = TEST_FILES['VALID_TEXT']
        self.invalid_file = TEST_FILES['INVALID_EXE']
        self.s3_config = S3_CONFIG

        self.valid_data = {
            'name': self.test_file['name'],
            'size': self.test_file['size'],
            'content': self.test_file['content'],
            'file_type': self.test_file['type'],
            's3_url': f"{self.s3_config['BUCKET_URL']}/{self.test_file['name']}",
            's3_etag': self.s3_config['TEST_ETAG'],
            's3_version_id': self.s3_config['TEST_VERSION'],
            's3_metadata': self.s3_config['TEST_METADATA']
        }

        self.invalid_data = {
            'name': self.invalid_file['name'],
            'size': self.invalid_file['size'],
            'content': self.invalid_file['content'],
            'file_type': self.invalid_file['type']
        }

    def test_valid_serializer(self):
        """Test serializer with valid data"""
        serializer = FileUploadSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_size(self):
        """Test serializer with invalid file size"""
        data = self.valid_data.copy()
        data['size'] = self.invalid_file['size']
        serializer = FileUploadSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('size', serializer.errors)

    def test_invalid_file_type(self):
        """Test serializer with invalid file type"""
        data = self.valid_data.copy()
        data['file_type'] = self.invalid_file['type']
        serializer = FileUploadSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('file_type', serializer.errors)