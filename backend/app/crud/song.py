from sqlalchemy.orm import Session, joinedload
from app import models

#Song
def get_song(db: Session, song_id: int):
    return db.query(models.Song).\
        options(joinedload(models.Song.album)).\
        options(joinedload(models.Song.artists)).\
        filter(models.Song.id == song_id).\
        first()

def get_songs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Song).\
        options(joinedload(models.Song.album)).\
        options(joinedload(models.Song.artists)).\
        offset(skip).\
        limit(limit).\
        all()