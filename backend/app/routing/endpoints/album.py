from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models
from app import schemas
from app import dependencies
# from .endpoint_item import album_endpoint
from app.crud.album import crud_album


router = APIRouter()

@router.get("/{id}", response_model=schemas.AlbumLoaded, include_in_schema=False)
@router.get("/{id}/", response_model=schemas.AlbumLoaded)
async def read_album(
        id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional)
    ):
    album = await crud_album.get(db, id, current_user)
    if album is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return album

@router.put("/{id}/like", include_in_schema=False, response_model=bool)
@router.put("/{id}/like/", response_model=bool)
async def like_album(
        id: int, 
        db: Session = Depends(dependencies.get_db), 
        current_user: schemas.User = Depends(dependencies.get_current_user)
    ):
    album = await crud_album.get(db, id, current_user)
    if album is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return await crud_album.like(db, id, current_user)

@router.get("", response_model=List[schemas.AlbumLoaded], include_in_schema=False)
@router.get("/", response_model=List[schemas.AlbumLoaded])
async def read_albums(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional)
    ):
    return await crud_album.get_all(db, skip, limit, current_user)
