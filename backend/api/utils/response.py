# api/utils/response.py
from rest_framework.response import Response
from datetime import datetime

def create_api_response(data=None, error=None, status=200, message=None):
    """
    Creates a standardized API response.
    
    Args:
        data: The data to return (default: None)
        error: Error message if any (default: None)
        status: HTTP status code (default: 200)
        message: Optional success message (default: None)
    
    Returns:
        Response: DRF Response object with standardized format
    """
    response_data = {
        'success': error is None,
        'timestamp': datetime.now().isoformat(),
        'data': data or {},
        'error': error,
        'message': message
    }
    
    return Response(response_data, status=status)