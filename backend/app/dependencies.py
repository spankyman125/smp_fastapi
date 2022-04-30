
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import schemas, security, models
from app.crud import user as crud_user
from app.database import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=True)
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)

def add_like_attr(user: models.User, objs_array, type):
    temp = objs_array
    liked_ids = []
    for i in range(len(getattr(user, type))):
        liked_ids.append(getattr(user, type)[i].id)
    for n in range(len(temp)):
        if temp[n].id in liked_ids:
            setattr(temp[n], "liked", True)
        else:
            setattr(temp[n], "liked", False)

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

token_expire_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        id: int = payload.get("id")
        username: str = payload.get("sub")
        if (username is None) or (id is None):
            raise credentials_exception
        user = schemas.UserReturn(id=id, username=username)
    except JWTError:
        raise token_expire_exception
    return user

async def get_current_user_optional(token: str = Depends(oauth2_scheme_optional)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        id: int = payload.get("id")
        username: str = payload.get("sub")
        if (username is None) or (id is None):
            raise credentials_exception
        user = schemas.UserReturn(id=id, username=username)
    except JWTError:
        raise token_expire_exception
    return user