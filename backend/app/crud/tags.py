from sqlalchemy.orm import Session, joinedload, lazyload

from app import models, schemas
from typing import Optional, List
from app.dependencies import add_like_attr

class TagCRUD():
    def get(self, db: Session, id: int):
        return "by_id"
    
    def get(self, db: Session, name: str):
        return "by_name"
    
    def get_all(self, db: Session):
        tags = db.query(models.Tag).all()
        return tags

    def get_songs(self, db: Session, tag: str):
        return "songs_by_tag"

<<<<<<< HEAD
    def get_songs(self, db: Session, tags: List[str], skip: int = 0, limit: int = 100, current_user: Optional[schemas.User] = None):
        songs = db.query(models.Song).\
            filter(models.Song.tags.any(models.Tag.name.in_(tags))).\
            offset(skip).\
            limit(limit).\
            all()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            for i in range(len(songs)):
                add_like_attr(current_db_user, [songs[i]], "songs")
=======
    def get_songs(self, db: Session, tags: List[str], skip: int = 0, limit: int = 100):
        songs = db.query(models.Song).\
            options(joinedload(models.Song.tags)).\
            filter(models.Tag.name.in_(tags)).\
            offset(skip).\
            limit(limit).\
            all()
>>>>>>> 4cf53c8431b6b9e68dc5b76657f59b0acfb8585c
        return songs

crud_tag = TagCRUD()
