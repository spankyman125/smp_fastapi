from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app import schemas
from app import dependencies

router = APIRouter()

@router.get("/{id}", response_model=schemas.ArtistRead)
def read_artist(id: int, db: Session = Depends(dependencies.get_db)):
    artist = crud.get_artist(db, artist_id=id)
    if artist is None:
        raise HTTPException(status_code=404, detail='Artist not found')
    return artist

@router.get("/", response_model=List[schemas.ArtistRead])
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    artists = crud.get_artists(db, skip=skip, limit=limit)
    return artists