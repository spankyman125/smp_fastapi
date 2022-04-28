
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import schemas, security
from app.crud import user as crud_user
from app.database import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
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
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        id: int = payload.get("id")
        username: str = payload.get("sub")
        if (username is None) or (id is None):
            raise credentials_exception
        user = schemas.UserReturn(id=id, username=username)
    except JWTError:
        raise token_expire_exception
    # user = crud_user.get_user(db, username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    return user

# async def test_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user