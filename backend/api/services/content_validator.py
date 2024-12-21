# api/services/content_validator.py
import re
from typing import List
from ..exceptions import FileValidationError

class ContentValidator:
    # Only the most critical SQL injection patterns that shouldn't appear in normal text
    SQL_KEYWORDS = [
        r'UNION\s+SELECT',
        r'INSERT\s+INTO.*VALUES',
        r'UPDATE.*SET',
        r'DROP\s+TABLE',
        r'DELETE\s+FROM',
        r'EXEC\s*\(',
        r'EXECUTE\s*\('
    ]
    
    # Only the most dangerous JavaScript/HTML patterns
    DANGEROUS_PATTERNS = [
        r'<script[\s>]',           # Script tags
        r'javascript:.*\(.*\)',    # JavaScript protocol with function calls
        r'data:text/html;base64,', # Base64 encoded HTML
        r'onload\s*=',             # Inline event handlers
        r'onerror\s*=',
        r'onclick\s*='
    ]

    @classmethod
    def validate_content(cls, content: str) -> None:
        """
        Validates file content for clearly malicious code patterns.
        Allows normal text content even if it contains technical terms.
        
        Args:
            content: The text content to validate
            
        Raises:
            FileValidationError: If clearly malicious content is detected
        """
        
        try:
            cls._check_sql_injection(content)
            cls._check_dangerous_patterns(content)
        except FileValidationError as e:
            # Add context to the error message
            raise FileValidationError(
                f"{str(e)}. If this is a legitimate file, please check for any "
                "embedded scripts or SQL queries that might trigger this security check."
            )
        
    @classmethod
    def _check_sql_injection(cls, content: str) -> None:
        """Check for obvious SQL injection patterns."""
        # Look for SQL patterns that combine multiple keywords
        # This reduces false positives for normal text containing SQL terms
        for pattern in cls.SQL_KEYWORDS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                
                if len(matches) > 0:
                    raise FileValidationError(
                        "File content contains multiple SQL command patterns"
                    )

    @classmethod
    def _check_dangerous_patterns(cls, content: str) -> None:
        """Check for clearly dangerous JavaScript/HTML patterns."""
        dangerous_pattern_count = 0
        
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                dangerous_pattern_count += 1
                
                # If we find multiple dangerous patterns, it's more likely to be malicious
                if dangerous_pattern_count > 1:
                    raise FileValidationError(
                        "File content contains multiple suspicious script-like patterns"
                    )