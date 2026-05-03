from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from core.config import settings

# In production, you would check this against a database.
# For now, we will use a secure key from the .env file.
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Add this to your .env file: API_SECRET_KEY=your_super_secret_key_here
VALID_API_KEYS = {settings.API_SECRET_KEY} if hasattr(settings, "API_SECRET_KEY") else {"test-key-123"}

async def verify_api_key(api_key_header: str = Security(api_key_header)):
    """
    Validates the incoming API key. 
    If missing or invalid, immediately returns a 403 Forbidden.
    """
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key is missing. Please provide the X-API-Key header."
        )
    
    if api_key_header not in VALID_API_KEYS:
        # SECURITY: Do not tell the user *why* it failed (e.g., don't say "Key not found in DB")
        # Just return a generic 403.
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials."
        )
        
    return api_key_header