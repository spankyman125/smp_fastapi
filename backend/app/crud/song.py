from sqlalchemy.orm import Session, joinedload
from app import models
from app.crud.base import ItemBase 

class SongCRUD(ItemBase):
    def get(self, db: Session, id: int):
        return db.query(self.model).\
            options(joinedload(self.model.album)).\
            options(joinedload(self.model.artists)).\
            filter(self.model.id == id).\
            first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).\
            options(joinedload(self.model.album)).\
            options(joinedload(self.model.artists)).\
            offset(skip).\
            limit(limit).\
            all()   

    def like(self, db: Session, id: int, user: models.User):
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

    def get_liked(self, user: models.User):
        return user.songs

crud_song = SongCRUD(model=models.Song, like_relation=models.UserSongLike)
