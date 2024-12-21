from django.test import TestCase
from api.models import FileUpload
from .test_constants import TEST_FILES, S3_CONFIG

class FileUploadModelTest(TestCase):
    def setUp(self):
        self.test_file = TEST_FILES['VALID_TEXT']
        self.s3_config = S3_CONFIG
        
        self.file_data = {
            'name': self.test_file['name'],
            'size': self.test_file['size'],
            'content': self.test_file['content'],
            'file_type': self.test_file['type'],
            's3_url': f"{self.s3_config['BUCKET_URL']}/{self.test_file['name']}",
            's3_etag': self.s3_config['TEST_ETAG'],
            's3_version_id': self.s3_config['TEST_VERSION'],
            's3_metadata': self.s3_config['TEST_METADATA']
        }
        self.file_upload = FileUpload.objects.create(**self.file_data)

    def test_file_upload_creation(self):
        """Test FileUpload model creation"""
        self.assertTrue(isinstance(self.file_upload, FileUpload))
        self.assertEqual(
            self.file_upload.__str__(), 
            f"{self.test_file['name']} ({self.test_file['size']}KB)"
        )

    def test_file_upload_fields(self):
        """Test all fields of FileUpload model"""
        self.assertEqual(self.file_upload.name, self.test_file['name'])
        self.assertEqual(self.file_upload.size, self.test_file['size'])
        self.assertEqual(self.file_upload.content, self.test_file['content'])
        self.assertEqual(self.file_upload.file_type, self.test_file['type'])
        self.assertEqual(self.file_upload.s3_etag, self.s3_config['TEST_ETAG'])
        self.assertEqual(self.file_upload.s3_version_id, self.s3_config['TEST_VERSION'])
        self.assertTrue(self.file_upload.uploaded_at)
        self.assertTrue(self.file_upload.last_modified)