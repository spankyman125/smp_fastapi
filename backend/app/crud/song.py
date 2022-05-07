from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.crud.base import ItemBase 
from app.dependencies import add_like_attr
from typing import Optional, List

class SongCRUD(ItemBase):
    def get(self, db: Session, id: int, current_user: Optional[schemas.UserReturn] = None):
        song = db.query(self.model).\
            options(joinedload(self.model.album)).\
            options(joinedload(self.model.artists)).\
            options(joinedload(self.model.tags)).\
            filter(self.model.id == id).\
            first()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, [song], "songs")
            add_like_attr(current_db_user, [song.album], "albums")
            add_like_attr(current_db_user, song.artists, "artists")
        return song

    def get_list(self, db:Session, id_list: List[int], current_user: Optional[schemas.UserReturn] = None, load: Optional[bool] = False):
        songs = db.query(models.Song).\
            filter(models.Song.id.in_(id_list))
        if load:
            songs.options(joinedload(models.Song.artists)).\
            options(joinedload(models.Song.album))
        songs.all()
        id_map = {t.id: t for t in songs}
        songs = [id_map[n] for n in id_list]
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            for i in range(len(songs)):
                add_like_attr(current_db_user, [songs[i]], "songs")
                if load:
                    add_like_attr(current_db_user, [songs[i].album], "albums")
                    add_like_attr(current_db_user, songs[i].artists, "artists")
        return songs

    def get_all(self, db: Session, skip: int = 0, limit: int = 100, current_user: Optional[schemas.UserReturn] = None):
        songs =  db.query(self.model).\
            options(joinedload(self.model.album)).\
            options(joinedload(self.model.artists)).\
            options(joinedload(self.model.tags)).\
            offset(skip).\
            limit(limit).\
            all()   
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            for i in range(len(songs)):
                add_like_attr(current_db_user, [songs[i]], "songs")
                add_like_attr(current_db_user, [songs[i].album], "albums")
                add_like_attr(current_db_user, songs[i].artists, "artists")
        return songs

    def like(self, db: Session, id: int, user: schemas.UserReturn):
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

    def get_liked(
        self,
        db:Session,
        user: schemas.UserReturn,
        current_user: Optional[schemas.UserReturn] = None
    ):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, db_user.songs, "songs")
        return db_user.songs

crud_song = SongCRUD(model=models.Song, like_relation=models.UserSongLike)
