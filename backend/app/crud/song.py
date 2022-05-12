from optparse import Option
from sqlalchemy.orm import Session, selectinload

from app import models, schemas
from app.crud.base import ItemBase 
from typing import Optional, List
import random

def add_like_attr(user: models.User, songs):
    liked_songs_id = []
    liked_albums_id = []
    liked_artists_id = []

    for liked_song in user.songs:
        liked_songs_id.append(liked_song.id)
    for liked_album in user.albums:
        liked_albums_id.append(liked_album.id)
    for liked_artist in user.artists:
        liked_artists_id.append(liked_artist.id)
    
    for song in songs:
        setattr(song, "liked", True) if song.id in liked_songs_id else setattr(song, "liked", False)
        setattr(song.album, "liked", True) if song.album.id in liked_albums_id else setattr(song.album, "liked", False)
        for artist in song.artists:
            setattr(artist, "liked", True) if artist.id in liked_artists_id else setattr(artist, "liked", False)

class SongCRUD(ItemBase):
    async def get(self, db: Session, id: int, current_user: Optional[schemas.User] = None):
        song = db.query(self.model).\
            options(selectinload(self.model.album)).\
            options(selectinload(self.model.artists)).\
            options(selectinload(self.model.tags)).\
            filter(self.model.id == id).\
            first()
        if current_user and song:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, [song])
        return song
    
    async def get_all(self, db: Session, skip: int = 0, limit: int = 100, current_user: Optional[schemas.User] = None):
        songs =  db.query(self.model).\
            options(selectinload(self.model.album)).\
            options(selectinload(self.model.artists)).\
            options(selectinload(self.model.tags)).\
            offset(skip).\
            limit(limit).\
            all()  
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, songs)
        return songs


    async def get_list(self, db:Session, id_list: List[int], current_user: Optional[schemas.User] = None, load: Optional[bool] = False):
        songs = db.query(models.Song).\
            filter(models.Song.id.in_(id_list))
        if load:
            songs.options(selectinload(models.Song.artists)).\
            options(selectinload(models.Song.album))
        songs.all()
        id_map = {t.id: t for t in songs}
        songs = [id_map[n] for n in id_list]
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, songs)
        return songs

    async def get_random(self, db:Session, limit: int = 10, current_user: Optional[schemas.User] = None, tags=None):
        song_count = db.query(self.model).count()
        random_id_list = random.sample(range(1, song_count), limit)
        if tags:
            songs = db.query(models.Song).\
                    filter(models.Song.tags.any(models.Tag.name.in_(tags))).\
                    filter(models.Song.id.in_(random_id_list)).\
                    all()
        else:
            songs = db.query(models.Song).\
                    filter(models.Song.id.in_(random_id_list)).\
                    all()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, songs)
        return songs

    async def like(self, db: Session, id: int, user: schemas.User):
        like = db.query(self.like_relation).get((user.id, id))
        if like:
            db.delete(like)
            db.commit()
            return False 
        else:
            like = self.like_relation(user_id=user.id, song_id=id)
            db.add(like)
            db.commit()
            db.refresh(like)
            return True 

    async def get_liked(
        self,
        db:Session,
        user: schemas.User,
        current_user: Optional[schemas.User] = None
    ):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, db_user.songs)
        return db_user.songs

crud_song = SongCRUD(model=models.Song, like_relation=models.UserSongLike)
