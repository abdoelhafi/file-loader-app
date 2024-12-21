class FileValidationConstants:
    # File size limits in bytes
    MIN_SIZE_BYTES = 512  # 0.5KB
    MAX_SIZE_BYTES = 2048  # 2KB
    
    # Content validation
    MAX_LINE_LENGTH = 1000
    ALLOWED_CONTENT_TYPE = 'text/plain'
    
    # File naming
    ALLOWED_EXTENSIONS = ['txt']
    MAX_FILENAME_LENGTH = 255

class ContentValidationMessages:
    INVALID_SIZE = "File size must be between 0.5KB and 2KB"
    INVALID_TYPE = "Only text files are allowed"
    INVALID_ENCODING = "File must be UTF-8 encoded"
    SUSPICIOUS_CONTENT = "File content contains suspicious patterns"
    INVALID_EXTENSION = "Only .txt files are allowed"