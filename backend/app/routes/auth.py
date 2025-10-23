from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from firebase_admin import auth
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


class UserResponse(BaseModel):
    uid: str
    email: str
    email_verified: bool
    display_name: str | None = None
    photo_url: str | None = None


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current user information
    """
    return UserResponse(
        uid=current_user["uid"],
        email=current_user["email"],
        email_verified=current_user.get("email_verified", False),
        display_name=current_user.get("name"),
        photo_url=current_user.get("picture"),
    )


@router.post("/verify-token")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verify Firebase ID token
    """
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return {
            "valid": True,
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email"),
            "email_verified": decoded_token.get("email_verified", False),
        }
    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase ID token",
        )
    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firebase ID token has expired",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}",
        )


@router.post("/refresh-token")
async def refresh_token(current_user: dict = Depends(get_current_user)):
    """
    Refresh user token (for validation; actual refresh is client-side)
    """
    return {
        "message": "Token is valid",
        "uid": current_user["uid"],
        "email": current_user.get("email"),
    }
