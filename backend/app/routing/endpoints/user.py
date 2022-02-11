from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.crud import artist as crud_artist

from app import schemas
from app import dependencies
from app import models

router = APIRouter()

@router.get("/me", response_model=schemas.UserAll)
def return_current_user(current_user: models.User = Depends(dependencies.get_current_user)):
    return current_user

@router.get("/me/artists", response_model=List[schemas.ArtistBase])
def read_artists_liked(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    artists = crud_artist.get_artists_liked(db, skip=skip, limit=limit, user=current_user)
    return artists

@router.get("/{username}/artists", response_model=List[schemas.ArtistBase])
def read_artists_liked(username: str ,skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(dependencies.get_current_user)):
    db_user = crud_user.get_user(db, username=username)
    artists = crud_artist.get_artists_liked(db, skip=skip, limit=limit, user=db_user)
    return artists

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

