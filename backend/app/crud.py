from sqlalchemy.orm import Session

from . import models

def get_song(db: Session, song_id:int):
    return db.query(models.Song).filter(models.Song.id == song_id).first()

def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album.id == album_id).first()

def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist.id == artist_id).first()