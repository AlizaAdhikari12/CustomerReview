from fastapi import Depends,status,HTTPException
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


def get_currentuser(
    credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
    token = credentials.credentials

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload

    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token"
        )

def require_customer(current_user: dict = Depends(get_currentuser)):
    if current_user.get('role')!="User":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Must be login as User to fill the review form"
        )

def require_admin(current_user : dict = Depends(get_currentuser)):
    if current_user.get('role')!="Admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Admin access required"
        )
        return current_user
