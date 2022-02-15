from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app import schemas
from app import dependencies
from .endpoint_item import album_endpoint

router = APIRouter()

@router.get("/{id}", response_model=schemas.AlbumRead)
def read_album(
        id: int,
        db: Session = Depends(dependencies.get_db)
    ):
    return album_endpoint.read(db, id)

@router.put("/{id}/like")
def like_artist(
        id: int, 
        db: Session = Depends(dependencies.get_db), 
        current_user: models.User = Depends(dependencies.get_current_user)
    ):
    return album_endpoint.like(db, id, current_user)

@router.get("/", response_model=List[schemas.AlbumRead])
def read_albums(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    return album_endpoint.read_all(db, skip, limit)
