from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import song as crud_song
from app import schemas
from app import dependencies

router = APIRouter()

@router.get("/{id}", response_model=schemas.SongRead)
def read_song(id: int, db: Session = Depends(dependencies.get_db)):
    song = crud_song.get_song(db, song_id=id)
    if song is None:
        raise HTTPException(status_code=404, detail='Song not found')
    return song

@router.get("/", response_model=List[schemas.SongRead])
def read_songs(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    songs = crud_song.get_songs(db, skip=skip, limit=limit)
    return songs