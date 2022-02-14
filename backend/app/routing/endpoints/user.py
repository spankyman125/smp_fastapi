from ctypes.wintypes import tagSIZE
from re import A
from typing import List
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.crud import artist as crud_artist

from app import schemas
from app import dependencies
from app import models

router = APIRouter()
router_me = APIRouter()
router_others = APIRouter()

@router_me.get("/me/artists", response_model=List[schemas.ArtistBase])
def read_artists_by_self(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user)
    ):
    artists = crud_artist.get_artists_liked(db, skip=skip, limit=limit, user=current_user)
    return artists
    

@router_others.get("/{username}/artists", response_model=List[schemas.ArtistBase])
def read_artists_by_username(
    username: Optional[str] = None,
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(dependencies.get_db)
    ):
    db_user = crud_user.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    artists = crud_artist.get_artists_liked(db, skip=skip, limit=limit, user=db_user)
    return artists


@router_me.get("/me", response_model=schemas.UserAll)
def read_user_self(
    current_user: models.User = Depends(dependencies.get_current_user)
    ):
    return current_user


@router_others.get("/{username}", response_model=schemas.UserAll)
def read_user_by_username(
    username: Optional[str] = None, 
    db: Session = Depends(dependencies.get_db)
    ):
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

