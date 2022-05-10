from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import dependencies, schemas, security, models
from app.crud import user as crud_user

router = APIRouter()

@router.post("/token", response_model=schemas.Token, include_in_schema=False)
@router.post("/token/", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = crud_user.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    refresh_token = security.create_refresh_token()
    user.refresh_token = refresh_token
    db.commit()
    db.flush()
    access_token = security.create_access_token(
        data={"sub": user.username, "type":"access", "id": user.id}
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/token-refresh", response_model=schemas.Token, include_in_schema=False)
@router.post("/token-refresh/", response_model=schemas.Token)
async def refresh_tokens(refresh_token: str, db: Session = Depends(dependencies.get_db)):
    user = db.query(models.User).filter(models.User.refresh_token == refresh_token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    refresh_token_new = security.create_refresh_token()
    user.refresh_token = refresh_token_new
    db.commit()
    db.flush()
    access_token = security.create_access_token(
        data={"sub": user.username, "type":"access", "id": user.id}
    )
    return {"access_token": access_token, "refresh_token": refresh_token_new, "token_type": "bearer"}