from sqlalchemy.orm import Session, joinedload
from app import models

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

def get_artists_liked(db: Session, user: models.User , skip: int = 0, limit: int = 100) :
    return user.artists

def like_artist(db: Session, artist_id: int, user: models.User):
    like = db.query(models.UserArtistLike).get((user.id, artist_id))
    if like:
        db.delete(like)
        db.commit()
        return False 
    else:
        like = models.UserArtistLike(user_id=user.id, artist_id=artist_id)
        db.add(like)
        db.commit()
        db.refresh(like)
        return True