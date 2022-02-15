from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, models, dependencies
from .endpoint_item import song_endpoint

router = APIRouter()

@router.get("/{id}", response_model=schemas.SongRead)
def read_song(
        id: int, 
        db: Session = Depends(dependencies.get_db)
    ):
    return song_endpoint.read(db, id)

@router.put("/{id}/like")
def like_song(
        id: int, 
        db: Session = Depends(dependencies.get_db), 
        current_user: models.User = Depends(dependencies.get_current_user)
    ):
    return song_endpoint.like(db, id, current_user)

@router.get("/", response_model=List[schemas.SongRead])
def read_songs(
        skip: int = 0, 
        limit: int = 100, 
        db: Session = Depends(dependencies.get_db)
    ):
    return song_endpoint.read_all(db, skip, limit)