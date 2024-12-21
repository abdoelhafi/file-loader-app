# Backend Features

## Table of Contents
- [Atomic Transactions](#atomic-transactions)
- [Security & Validation](#security-and-validation)
- [Error Handling System](#error-handling-system)

## Atomic Transactions

The core feature of the backend is its atomic transaction system that ensures data consistency between AWS S3 and RDS:

```python
@transaction.atomic
def create_file(self, file_obj) -> FileUpload:
    # Validate file
    self._validate_file(file_obj)
    content = self._read_and_validate_file_content(file_obj)

    # Create transaction savepoint
    sid = transaction.savepoint()
    
    try:
        # Upload to S3
        s3_url, s3_metadata = self.s3_service.upload_file(
            file_obj,
            unique_filename,
            file_obj.content_type,
            metadata
        )

        # Create database record
        file_upload = FileUpload.objects.create(
            name=file_obj.name,
            s3_url=s3_url,
            s3_metadata=metadata
        )

        transaction.savepoint_commit(sid)
        return file_upload

    except Exception as e:
        # Rollback and cleanup
        transaction.savepoint_rollback(sid)
        self.s3_service.delete_file(unique_filename)
        raise
```

Key Features:
- Transaction savepoints for rollback capability
- Automatic S3 cleanup on failure
- Consistent state between S3 and database
- Error recovery mechanisms

## Security and Validation

### File Validation Pipeline
```python
def _validate_file(self, file_obj) -> None:
    # Size validation
    if not (MIN_SIZE_BYTES <= file_obj.size <= MAX_SIZE_BYTES):
        raise FileValidationError(INVALID_SIZE)
    
    # Content type validation
    if file_obj.content_type != ALLOWED_CONTENT_TYPE:
        raise FileValidationError(INVALID_TYPE)
    
    # Extension validation
    extension = file_obj.name.split('.')[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise FileValidationError(INVALID_EXTENSION)
```

Security Measures:
- Strict file size limits (0.5KB to 2KB)
- Content type verification
- File extension validation
- UTF-8 encoding validation
- SQL injection prevention through ORM
- S3 metadata sanitization

## Error Handling System

### Custom Exception Hierarchy
```python
class FileValidationError(Exception):
    # File validation specific errors
    pass

class StorageError(Exception):
    # S3 storage operation errors
    pass
```

Error Categories:
1. **Validation Errors**
   - Size violations
   - Type mismatches
   - Content validation failures

2. **Storage Errors**
   - S3 upload failures
   - Database transaction errors
   - Cleanup failures

Each error is logged with detailed information for debugging and monitoring:
```python
logger.warning(f"Content validation failed: {str(e)}")
logger.error(f"Failed to cleanup S3 file: {cleanup_error}")
```