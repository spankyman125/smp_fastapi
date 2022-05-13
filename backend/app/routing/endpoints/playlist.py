from urllib import response
import uuid
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app import schemas, models, dependencies
from app.crud.playlist import crud_playlist

router = APIRouter()

@router.get("", response_model=List[schemas.Playlist], include_in_schema=False)
@router.get("/", response_model=List[schemas.Playlist])
async def read_playlists(
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user),
    ):
    return await crud_playlist.get_all(db, current_user)

@router.get("/{id}",response_model=schemas.PlaylistLoaded, include_in_schema=False)
@router.get("/{id}/",response_model=schemas.PlaylistLoaded)
async def read_playlist(
        id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user),
    ):
    return await crud_playlist.get(db, current_user, id)

@router.post("/{id}/upload-image", include_in_schema=False, response_model = schemas.PlaylistUpdateImage)
@router.post("/{id}/upload-image/", response_model = schemas.PlaylistUpdateImage)
async def upload_playlist_cover(
    id:int,
    file: UploadFile=File(...),
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user), 
):
    return await crud_playlist.update_playlist_image(db=db, user=current_user, playlist_id=id, file=file)

@router.post("/{id}/add", include_in_schema=False, response_model=schemas.Playlist)
@router.post("/{id}/add/", response_model=schemas.Playlist)
async def add_song(
        id: int,
        song_id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user),
    ):
    return await crud_playlist.add(db, current_user, song_id, id)

@router.post("/{id}/add-list", include_in_schema=False, response_model=schemas.Playlist)
@router.post("/{id}/add-list/", response_model=schemas.Playlist)
async def add_songs(
        id: int,
        song_list: List[int],
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user),
    ):
    return await crud_playlist.add_list(db=db, user=current_user, song_list=song_list, playlist_id=id)

@router.post("", include_in_schema=False, response_model=schemas.Playlist)
@router.post("/", response_model=schemas.Playlist)
async def create_playlist(
        name: str,
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user),
    ):
    return await crud_playlist.create(db, current_user, name)

@router.delete("/{id}", include_in_schema=False,  response_model=bool)
@router.delete("/{id}/", response_model=bool)
async def delete_playlist(
        id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user),
    ):
    return await crud_playlist.delete(db, current_user, id)

@router.delete("/{id}/clear", include_in_schema=False, response_model=schemas.Playlist)
@router.delete("/{id}/clear/", response_model=schemas.Playlist)
async def clear_playlist(
        id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user),
    ):
    return await crud_playlist.clear(db, current_user, id)

@router.delete("/{id}/delete", include_in_schema=False, response_model=schemas.Playlist)
@router.delete("/{id}/delete/", response_model=schemas.Playlist)
async def remove_song(
        id: int,
        position: int,
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user),
    ):
    return await crud_playlist.remove(db, current_user, position, id)
