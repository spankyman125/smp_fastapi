from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app import dependencies

router = APIRouter()

@router.get("/{id}", response_model=schemas.AlbumRead)
def read_album(id: int, db: Session = Depends(dependencies.get_db)):
    album = crud.get_album(db, album_id=id)
    if album is None:
        raise HTTPException(status_code=404, detail='Album not found')
    return album

@router.get("/", response_model=List[schemas.AlbumRead])
def read_songs(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    songs = crud.get_albums(db, skip=skip, limit=limit)
    return songs