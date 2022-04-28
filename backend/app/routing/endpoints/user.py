from typing import List
from urllib import response

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session

from app import schemas, dependencies, models, main
from app.crud import user as crud_user
from app.crud.artist import crud_artist
from app.crud.song import crud_song
from app.crud.album import crud_album 
import uuid

router = APIRouter()
router_me = APIRouter()
router_others = APIRouter()

@router_me.get("/me", response_model=schemas.UserAll)
def read_user_self(
    current_user: schemas.UserReturn = Depends(dependencies.get_current_user),
    db: Session = Depends(dependencies.get_db)
):
    db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
    return db_user

@router_me.post("/me", response_model=schemas.UserAbout)
def update_user_about(
    user_about: schemas.UserAbout,
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.UserReturn = Depends(dependencies.get_current_user), 
):
    return crud_user.update_user(db, user=current_user, user_about=user_about)

@router_me.post("/me/upload-image", response_model=schemas.UserUpdateImage)
async def upload_avatar(
    file: UploadFile=File(...),
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.UserReturn = Depends(dependencies.get_current_user), 
):
    return await crud_user.update_user_avatar(db, user=current_user, file=file)

@router_me.get("/me/artists", response_model=List[schemas.ArtistBase])
def read_artists_by_self(
    current_user: schemas.UserReturn = Depends(dependencies.get_current_user),
    db: Session = Depends(dependencies.get_db)
): 
    return crud_artist.get_liked(db=db, user=current_user)

@router_me.get("/me/songs", response_model=List[schemas.SongBase])
def read_songs_by_self(
    current_user: schemas.UserReturn = Depends(dependencies.get_current_user),
    db: Session = Depends(dependencies.get_db)
):
    return crud_song.get_liked(db=db, user=current_user)

@router_me.get("/me/albums", response_model=List[schemas.AlbumBase])
def read_albums_by_self(
    current_user: schemas.UserReturn = Depends(dependencies.get_current_user),
    db: Session = Depends(dependencies.get_db)
):
    return crud_album.get_liked(db=db, user=current_user)

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
    return crud_artist.get_liked(db=db, user=db_user)

@router_others.get("/{username}/songs", response_model=List[schemas.SongBase])
def read_songs_by_username(
        username: str,
        db: Session = Depends(dependencies.get_db)
    ):
    db_user = crud_user.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud_song.get_liked(db=db, user=db_user)

@router_others.get("/{username}/albums", response_model=List[schemas.AlbumBase])
def read_albums_by_username(
        username: str,
        db: Session = Depends(dependencies.get_db)
    ):
    db_user = crud_user.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud_album.get_liked(db=db, user=db_user)

@router.post("/", response_model=schemas.UserAll)
def create_user(
        user: schemas.UserCreate, 
        db: Session = Depends(dependencies.get_db)
    ):
    db_user = crud_user.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud_user.create_user(db=db, user=user)