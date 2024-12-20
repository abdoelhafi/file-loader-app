from django.db import models

class FileUpload(models.Model):
    name = models.CharField(max_length=255)
    size = models.FloatField() 
    content = models.TextField()  
    file_type = models.CharField(max_length=50)
    s3_url = models.URLField(max_length=1000)
    s3_etag = models.CharField(max_length=100, null=True)
    s3_version_id = models.CharField(max_length=100, null=True)
    s3_metadata = models.JSONField(default=dict)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['uploaded_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.size}KB)"