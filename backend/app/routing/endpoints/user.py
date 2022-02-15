from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import user as crud_user
from app.crud.artist import crud_artist
from app.crud.song import crud_song
from app.crud.album import crud_album 
# from app.crud.playlist import crud_playlist

from app import schemas
from app import dependencies
from app import models

router = APIRouter()
router_me = APIRouter()
router_others = APIRouter()


@router_me.get("/me", response_model=schemas.UserAll)
def read_user_self(current_user: models.User = Depends(dependencies.get_current_user)):
    return current_user

@router_me.get("/me/artists", response_model=List[schemas.ArtistBase])
def read_artists_by_self(current_user: models.User = Depends(dependencies.get_current_user)): 
    return crud_artist.get_liked(user=current_user)

@router_me.get("/me/songs", response_model=List[schemas.SongBase])
def read_songs_by_self(current_user: models.User = Depends(dependencies.get_current_user)):
    return crud_song.get_liked(user=current_user)

@router_me.get("/me/albums", response_model=List[schemas.AlbumBase])
def read_albums_by_self(current_user: models.User = Depends(dependencies.get_current_user)):
    return crud_album.get_liked(user=current_user)

# @router_me.get("/me/playlists", response_model=List[schemas.PlaylistBase])
# def read_albums_by_self(current_user: models.User = Depends(dependencies.get_current_user)):
#     return crud_album.get_liked(user=current_user)

@router_others.get("/{username}", response_model=schemas.UserAll)
def read_user_by_username(
        username: str, 
        db: Session = Depends(dependencies.get_db)
    ):
    user = crud_user.get_user(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router_others.get("/{username}/artists", response_model=List[schemas.ArtistBase])
def read_artists_by_username(
        username: str,
        db: Session = Depends(dependencies.get_db)
    ):
    db_user = crud_user.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud_artist.get_liked(user=db_user)

@router_others.get("/{username}/songs", response_model=List[schemas.SongBase])
def read_songs_by_username(
        username: str,
        db: Session = Depends(dependencies.get_db)
    ):
    db_user = crud_user.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud_song.get_liked(user=db_user)

@router_others.get("/{username}/albums", response_model=List[schemas.AlbumBase])
def read_albums_by_username(
        username: str,
        db: Session = Depends(dependencies.get_db)
    ):
    db_user = crud_user.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud_album.get_liked(user=db_user)

@router.post("/", response_model=schemas.UserAll)
def create_user(
        user: schemas.UserCreate, 
        db: Session = Depends(dependencies.get_db)
    ):
    db_user = crud_user.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud_user.create_user(db=db, user=user)