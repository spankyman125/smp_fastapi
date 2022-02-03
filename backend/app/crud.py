from sqlalchemy.orm import Session, joinedload
from . import models, schemas
from passlib.context import CryptContext
# from .main import pwd_context

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

#Album
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

#Artist
def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).\
        options(joinedload(models.Artist.songs)).\
        options(joinedload(models.Artist.albums)).\
        filter(models.Artist.id == artist_id).\
        first()

def get_artists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artist).\
        options(joinedload(models.Artist.songs)).\
        options(joinedload(models.Artist.albums)).\
        offset(skip).\
        limit(limit).\
        all()

#Auth
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, pwd_context: CryptContext ):
    password_hash = pwd_context.hash(user.password)
    db_user = models.User(password_hash=password_hash, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user