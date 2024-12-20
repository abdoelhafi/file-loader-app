# api/serializers.py
from rest_framework import serializers
from .models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = [
            'id', 
            'name', 
            'size', 
            'content', 
            'file_type',
            's3_url',
            's3_etag',
            's3_version_id',
            's3_metadata',
            'uploaded_at',
            'last_modified'
        ]
        read_only_fields = ['uploaded_at', 'last_modified']

    def validate(self, data):
        # Validate file size (0.5KB to 2KB)
        if data['size'] < 0.5 or data['size'] > 2:
            raise serializers.ValidationError({
                "size": "File size must be between 0.5KB and 2KB"
            })
        
        # Validate file type
        if data['file_type'] != 'text/plain':
            raise serializers.ValidationError({
                "file_type": "Only text files are allowed"
            })
        
        return data