import datetime

from fastapi import APIRouter, Depends, Query
from app import main, dependencies, schemas
from typing import List, Optional
from sqlalchemy.orm import joinedload, Session
from app.crud.song import crud_song 
from app.crud.album import crud_album
from app.crud.artist import  crud_artist

router = APIRouter()

@router.get("/random/albums", response_model=List[schemas.Album], include_in_schema=False)
@router.get("/random/albums/", response_model=List[schemas.Album])
async def get_random_albums(
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user_optional),
    limit: Optional[int]=10
):
    return crud_album.get_random(db, limit, current_user)

@router.get("/random/song", response_model=List[schemas.SongLoaded], include_in_schema=False)
@router.get("/random/songs/", response_model=List[schemas.SongLoaded])
async def get_random_songs_by_tags(
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user_optional),
    limit: Optional[int]=10,
    tags: Optional[List[str]]=Query([])
):
    return crud_song.get_random(db, limit, current_user,tags)

@router.get("/random/artists", response_model=List[schemas.Artist], include_in_schema=False)
@router.get("/random/artists/", response_model=List[schemas.Artist])
async def get_random_artists(
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user_optional),
    limit: Optional[int]=10
):
    return crud_artist.get_random(db, limit, current_user)
    

@router.get("/last-album-releases", response_model=List[schemas.Album], include_in_schema=False)
@router.get("/last-album-releases/", response_model=List[schemas.Album])
async def get_last_album_releases(
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user_optional),
    limit: Optional[int]=10
):
    return crud_album.get_last_releases(db, limit, current_user)
    
