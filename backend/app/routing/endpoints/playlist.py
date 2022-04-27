from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, models, dependencies
from app.crud.playlist import crud_playlist

router = APIRouter()

@router.get("/", response_model=List[schemas.PlaylistAll])
def read_playlists(
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_playlist.get_all(current_user)

@router.get("/{id}")
def read_playlist(
        id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_playlist.get(db, current_user, id)

@router.post("/{id}/add")
def add_song(
        id: int,
        song_id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_playlist.add(db, current_user, song_id, id)

@router.post("/{id}/add-list")
def add_songs(
        id: int,
        song_list: List[int],
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_playlist.add_list(db=db, user=current_user, song_list=song_list, playlist_id=id)

@router.post("/")
def create_playlist(
        name: str,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_playlist.create(db, current_user, name)

@router.delete("/{id}")
def delete_playlist(
        id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_playlist.delete(db, current_user, id)

@router.delete("/{id}/delete")
def remove_song(
        id: int,
        position: int,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_playlist.remove(db, current_user, position, id)