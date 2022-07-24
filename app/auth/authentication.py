from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from app.db.database import get_db
from app.db.models import user_management as models
from app.auth.hash import Hash
from app.auth import oauth2, schema_oauth as schemas
from app.api.crud.user_management import get_payload_token_by_username

router = APIRouter(
    tags=['Authentication'],
    prefix="/Authentication"
)


@router.post('/login')
def get_token_with_login(request: schemas.Login, db: Session = Depends(get_db)):
    user = db.query(models.UserAccount).filter(models.UserAccount.account_name == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if user.status == 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User status is inactive")
    if not Hash.verify(user.password_hash, request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    data = get_payload_token_by_username(username=user.account_name, on_behalf_of=request.onAccountOf, db=db)
    access_token = oauth2.create_access_token(data=data)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'username': user.account_name
    }

@router.post('/login-swagger', include_in_schema=False)
def get_token_with_login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.UserAccount).filter(models.UserAccount.account_name == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if user.status == 2:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User status is inactive")
    if not Hash.verify(user.password_hash, request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    data = get_payload_token_by_username(username=user.account_name, on_behalf_of=None, db=db)
    access_token = oauth2.create_access_token(data=data)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'username': user.account_name
    }
