from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas, models, dependencies
from app.crud.queue import crud_queue

router = APIRouter()

@router.get("/")
def read_queue(
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user)
    ):
    return crud_queue.get(db, current_user)

@router.post("/add")
def add_song_to_queue(
        song_id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_queue.add(db, current_user, song_id)

# @router.put("/replace")
# def replace_queue(
#         list: schemas.SongList,
#         db: Session = Depends(dependencies.get_db),
#         current_user: models.User = Depends(dependencies.get_current_user),
#     ):
#     return crud_queue.replace(current_user)

@router.delete("/delete")
def delete_song_from_queue(
        position: int,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_queue.delete(db, current_user, position)