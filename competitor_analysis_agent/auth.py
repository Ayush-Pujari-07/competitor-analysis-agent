import os
from fastapi import Request
from jose import jwt, JWTError
from fastapi import HTTPException

class TokenVerificationError(HTTPException):
    """Custom exception class for token verification errors."""

    def __init__(self, detail: str = "Token verification failed"):
        super().__init__(status_code=401, detail=detail)


def verify_token(api_key: str) -> None:
    """
    Verify the JWT token.
    """
    try:
        decoded_token = jwt.decode(api_key, os.getenv("SECRET_KEY"), algorithms=['HS256'])
    except JWTError as e:
        raise TokenVerificationError("Unauthorized user") from e


def authenticate_JWT(request: Request) -> None:
    """
    Middleware function to authenticate API keys.
    """
    # Extract headers
    api_key = request.headers.get("Api-Key")

    # Check if headers are present
    if api_key is None:
        raise HTTPException(status_code=401, detail="API Key is missing")

    # Verify JWT token
    verify_token(api_key)