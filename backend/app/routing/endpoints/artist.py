from typing import List
from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models
from app import schemas
from app import dependencies
# from .endpoint_item import artist_endpoint
from app.crud.artist import crud_artist


router = APIRouter()

@router.get("/{id}", response_model=schemas.ArtistLoaded, include_in_schema=False)
@router.get("/{id}/", response_model=schemas.ArtistLoaded)
async def read_artist(
        id: int, 
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional)
    ):
    artist = await crud_artist.get(db, id, current_user)
    if artist is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return artist

@router.put("/{id}/like", include_in_schema=False, response_model=bool)
@router.put("/{id}/like/", response_model=bool)
async def like_artist(
        id: int, 
        db: Session = Depends(dependencies.get_db), 
        current_user: schemas.User = Depends(dependencies.get_current_user)
    ):
    artist = await crud_artist.get(db, id, current_user)
    if artist is None:
        raise HTTPException(status_code=404, detail='Item not found')
    return crud_artist.like(db, id, current_user)

@router.get("", response_model=List[schemas.ArtistLoaded], include_in_schema=False)
@router.get("/", response_model=List[schemas.ArtistLoaded])
async def read_artists(
        skip: int = 0, 
        limit: int = 100, 
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional)
    ):
    return await crud_artist.get_all(db, skip, limit, current_user)
