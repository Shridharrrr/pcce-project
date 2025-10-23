from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}"
        )

async def get_current_user_websocket(token: str):
    """Get current user for WebSocket connections"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        return None