from sqlalchemy.orm import Session, joinedload
from app import models

def get_album(db: Session, album_id: int):
    return db.query(models.Album).\
        options(joinedload(models.Album.songs)).\
        options(joinedload(models.Album.artists)).\
        filter(models.Album.id == album_id).\
        first()

def get_albums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Album).\
        options(joinedload(models.Album.songs)).\
        options(joinedload(models.Album.artists)).\
        offset(skip).\
        limit(limit).\
        all()