TEST_FILES = {
    'VALID_TEXT': {
        'name': 'test.txt',
        'content': "x"*512,
        'size': 0.6,
        'type': 'text/plain'
    },
    'INVALID_EXE': {
        'name': 'test.exe',
        'content': 'test content',
        'size': 0.1,
        'type': 'application/exe'
    }
}

S3_CONFIG = {
    'BUCKET_URL': 'https://test-bucket.s3.amazonaws.com',
    'TEST_ETAG': 'test-etag',
    'TEST_VERSION': 'test-version',
    'TEST_METADATA': {'test': 'metadata'}
}