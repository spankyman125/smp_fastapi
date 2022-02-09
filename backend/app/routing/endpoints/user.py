from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import user as crud_user 
from app import schemas
from app import dependencies

router = APIRouter()

@router.get("/{username}", response_model=schemas.UserAll)
def read_user(username: str, db: Session = Depends(dependencies.get_db)):
    user = crud_user.get_user(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.post("/", response_model=schemas.UserAll)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud_user.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud_user.create_user(db=db, user=user)