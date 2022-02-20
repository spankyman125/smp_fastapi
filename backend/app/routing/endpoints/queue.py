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

@router.get("/current")
def read_current(
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_queue.current(db, current_user)

@router.post("/add")
def add_song_to_queue(
        song_id: int,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_queue.add(db, current_user, song_id)

@router.put("/next")
def next_track(
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_queue.next(db, current_user)

@router.put("/prev")
def previous_track(
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_queue.prev(db, current_user)

@router.put("/replace")
def replace(
        song_list: List[int],
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_queue.replace(db, current_user, song_list)

@router.delete("/delete")
def delete_song_from_queue(
        position: int,
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_queue.delete(db, current_user, position)

@router.delete("/clear")
def clear_queue(
        db: Session = Depends(dependencies.get_db),
        current_user: models.User = Depends(dependencies.get_current_user),
    ):
    return crud_queue.clear(db, current_user)