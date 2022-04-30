from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.crud.base import ItemBase 
from app.dependencies import add_like_attr
from typing import Optional

class ArtistCRUD(ItemBase):
    def get(self, db: Session, id: int, current_user: Optional[schemas.UserReturn] = None):
        artist = db.query(self.model).\
            options(joinedload(self.model.songs)).\
            options(joinedload(self.model.albums)).\
            filter(self.model.id == id).\
            first()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, [artist], "artists")
            add_like_attr(current_db_user, artist.albums, "albums")
            add_like_attr(current_db_user, artist.songs, "songs")
        return artist
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100, current_user: Optional[schemas.UserReturn] = None):
        artists = db.query(self.model).\
            options(joinedload(self.model.songs)).\
            options(joinedload(self.model.albums)).\
            offset(skip).\
            limit(limit).\
            all() 
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            for i in range(len(artists)):
                add_like_attr(current_db_user, [artists[i]], "artists")
                add_like_attr(current_db_user, artists[i].albums, "albums")
                add_like_attr(current_db_user, artists[i].songs, "songs")
        return artists

    def like(self, db: Session, id: int, user: schemas.UserReturn):
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
        user: schemas.UserReturn,
        current_user: Optional[schemas.UserReturn] = None
    ):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, db_user.artists, "artists")
        return db_user.artists

crud_artist = ArtistCRUD(models.Artist, models.UserArtistLike)