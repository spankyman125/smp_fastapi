from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app import schemas
from app import dependencies
from app.crud.tags import crud_tag
from typing import List, Optional

router = APIRouter()

@router.get("/")
def get_tags(
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional)
    ):
    return crud_tag.get_all(db)

@router.get("/songs", response_model=List[schemas.SongTagged])
def get_songs_by_tags(
        skip: int = 0, 
        limit: int = 100, 
        tags: List[str]=Query([]),
        db: Session = Depends(dependencies.get_db),
        current_user: schemas.User = Depends(dependencies.get_current_user_optional),
    ):
<<<<<<< HEAD
    return crud_tag.get_songs(db=db, skip=skip, limit=limit, tags=tags, current_user=current_user)
=======
    return crud_tag.get_songs(db=db, skip=skip, limit=limit, tags=tags)
>>>>>>> 4cf53c8431b6b9e68dc5b76657f59b0acfb8585c
