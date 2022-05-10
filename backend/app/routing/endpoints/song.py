from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import schemas, models, dependencies
from app.crud.song import crud_song
# from .endpoint_item import song_endpoint

router = APIRouter()

@router.get("/{id}", response_model=schemas.SongLoaded, include_in_schema=False)
@router.get("/{id}/", response_model=schemas.SongLoaded)
def read_song(
        id: int, 
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional)
    ):
    song = crud_song.get(db, id, current_user)
    if song is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return song

@router.put("/{id}/like", include_in_schema=False)
@router.put("/{id}/like/")
def like_song(
        id: int, 
        db: Session = Depends(dependencies.get_db), 
        current_user: schemas.User = Depends(dependencies.get_current_user)
    ):
    song = crud_song.get(db, id, current_user)
    if song is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return crud_song.like(db, id, current_user)

@router.get("", response_model=List[schemas.SongLoaded], include_in_schema=False)
@router.get("/", response_model=List[schemas.SongLoaded])
def read_songs(
        skip: int = 0, 
        limit: int = 100, 
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional)
    ):
    return crud_song.get_all(db, skip, limit, current_user)