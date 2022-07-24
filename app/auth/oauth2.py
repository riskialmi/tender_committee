from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt
from jose.exceptions import JWTError
from app.api.crud.user_management import get_user_by_account_name, get_user_by_email
from app.db.database import get_db
from app.system.config import SECRET_KEY, ALGORITHM, EMAIL_ADMIN

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Authentication/login-swagger")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("account_name")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_account_name(username, db)

    if user is None:
        raise credentials_exception

    return {'user': user.account_name,
            'on_behalf_of': payload.get("on_behalf_of")
            }

def fake_auth_user(db: Session = Depends(get_db)):
    user = get_user_by_email(EMAIL_ADMIN[0], db)
    return {'user': user.account_name,
            'on_behalf_of': user.account_name
            }
