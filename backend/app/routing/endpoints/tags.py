from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app import schemas
from app import dependencies
from app.crud.tags import crud_tag
from typing import List, Optional

router = APIRouter()

@router.get("", response_model=List[schemas.Tag], include_in_schema=False)
@router.get("/", response_model=List[schemas.Tag])
async def get_tags(
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional)
    ):
    return await crud_tag.get_all(db)

@router.get("/songs", response_model=List[schemas.SongLoaded], include_in_schema=False)
@router.get("/songs/", response_model=List[schemas.SongLoaded])
async def get_songs_by_tags(
        skip: int = 0, 
        limit: int = 100, 
        tags: List[str]=Query([]),
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional),
    ):
    return await crud_tag.get_songs(db=db, skip=skip, limit=limit, tags=tags, current_user=current_user)