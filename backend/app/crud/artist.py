from sqlalchemy.orm import Session, selectinload
import random
from app import models, schemas
from app.crud.base import ItemBase 
from typing import Optional, List

def add_like_attr(user: models.User, artists):
    liked_songs_id = []
    liked_albums_id = []
    liked_artists_id = []

    for liked_song in user.songs:
        liked_songs_id.append(liked_song.id)
    for liked_album in user.albums:
        liked_albums_id.append(liked_album.id)
    for liked_artist in user.artists:
        liked_artists_id.append(liked_artist.id)
    
    for artist in artists:
        setattr(artist, "liked", True) if artist.id in liked_artists_id else setattr(artist, "liked", False)
        for album in artist.albums:
            setattr(album, "liked", True) if album.id in liked_albums_id else setattr(album, "liked", False)
        for song in artist.songs:
            setattr(song, "liked", True) if song.id in liked_songs_id else setattr(song, "liked", False)
            setattr(song.album, "liked", True) if song.album.id in liked_albums_id else setattr(song.album, "liked", False)
            for artist in song.artists:
                setattr(artist, "liked", True) if artist.id in liked_artists_id else setattr(artist, "liked", False)


class ArtistCRUD(ItemBase):
    def get(self, db: Session, id: int, current_user: Optional[schemas.User] = None):
        artist = db.query(self.model).\
            options(selectinload(self.model.songs)).\
            options(selectinload(self.model.albums)).\
            filter(self.model.id == id).\
            first()
        if current_user and artist:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, [artist])
        return artist
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100, current_user: Optional[schemas.User] = None):
        artists = db.query(self.model).\
            options(selectinload(self.model.songs)).\
            options(selectinload(self.model.albums)).\
            offset(skip).\
            limit(limit).\
            all() 
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, artists)
        return artists

    def get_list(self, db:Session, id_list: List[int], current_user: Optional[schemas.User] = None):
        artists = db.query(models.Artist).\
            filter(models.Artist.id.in_(id_list)).\
            all()
        id_map = {t.id: t for t in artists}
        artists = [id_map[n] for n in id_list]
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, artists)
        return artists

    def get_random(self, db:Session, limit: int = 10, current_user: Optional[schemas.User] = None):
        artist_count = db.query(self.model).count()
        random_id_list = random.sample(range(1, artist_count), limit)
        artists = db.query(models.Artist).\
            filter(models.Artist.id.in_(random_id_list)).\
            all()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, artists)
        return artists

    def like(self, db: Session, id: int, user: schemas.User):
        like = db.query(self.like_relation).get((user.id, id))
        if like:
            db.delete(like)
            db.commit()
            return False 
        else:
            like = self.like_relation(user_id=user.id, artist_id=id)
            db.add(like)
            db.commit()
            db.refresh(like)
            return True 

    def get_liked(
        self,
        db:Session,
        user: schemas.User,
        current_user: Optional[schemas.User] = None
    ):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, db_user.artists)
        return db_user.artists

crud_artist = ArtistCRUD(models.Artist, models.UserArtistLike)