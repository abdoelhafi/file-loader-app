from django.test import TestCase
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from .test_constants import TEST_FILES

class FileUploadIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_file = SimpleUploadedFile(
            TEST_FILES['VALID_TEXT']['name'],
            TEST_FILES['VALID_TEXT']['content'].encode(),
            content_type=TEST_FILES['VALID_TEXT']['type']
        )

    def test_upload_list_delete_flow(self):
        """Test complete flow: upload file, list it, then delete it"""
        # 1. Upload file
        upload_response = self.client.post(
            '/api/files/',
            {'file': self.test_file},
            format='multipart'
        )
        self.assertEqual(upload_response.status_code, 201)
        file_id = upload_response.data['data']['id']

        # 2. Verify file appears in list
        list_response = self.client.get('/api/files/')
        self.assertEqual(list_response.status_code, 200)
        self.assertTrue(any(f['id'] == file_id for f in list_response.data['data']))

        # 3. Delete file
        delete_response = self.client.delete(f'/api/files/{file_id}/')
        self.assertEqual(delete_response.status_code, 204)

        # 4. Verify file is gone from list
        list_response = self.client.get('/api/files/')
        self.assertFalse(any(f['id'] == file_id for f in list_response.data['data']))
        
class ErrorHandlingIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_invalid_file_type_handling(self):
        """Test system's handling of invalid file types"""
        invalid_file = SimpleUploadedFile(
            "test.exe",
            b"Invalid content",
            content_type="application/exe"
        )
        
        response = self.client.post(
            '/api/files/',
            {'file': invalid_file},
            format='multipart'
        )
        self.assertEqual(response.status_code, 400)

    def test_large_file_handling(self):
        """Test system's handling of files exceeding size limit"""
        large_content = b"x" * (2 * 1024 * 1024)  # 2MB file
        large_file = SimpleUploadedFile(
            "large.txt",
            large_content,
            content_type="text/plain"
        )
        
        response = self.client.post(
            '/api/files/',
            {'file': large_file},
            format='multipart'
        )
        self.assertEqual(response.status_code, 400)