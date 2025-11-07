from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud, models
from .config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from .database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

ALGORITHM = "HS256"


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    """Create a JWT access token. expires_delta is minutes (optional)."""
    to_encode = data.copy()
    minutes = expires_delta if expires_delta is not None else ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_any = payload.get("sub")
        # payload.get may return None/Any; ensure it's a str
        if not isinstance(email_any, str):
            raise credentials_exception
        email: str = email_any
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token expired", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    # Use getattr to satisfy static analyzers which see Column[bool] on model class
    if not getattr(current_user, "is_active", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_admin(current_user: models.User = Depends(get_current_active_user)):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(
            status_code=403, detail="Admin privileges required")
    return current_user
