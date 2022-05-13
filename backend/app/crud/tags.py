from sqlalchemy.orm import Session, joinedload, lazyload

from app import models, schemas
from typing import Optional, List
from app.crud.song import add_like_attr

class TagCRUD():
    async def get(self, db: Session, id: int):
        return "by_id"
    
    async def get(self, db: Session, name: str):
        return "by_name"
    
    async def get_all(self, db: Session):
        tags = db.query(models.Tag).all()
        return tags

    async def get_songs(self, db: Session, tag: str):
        return "songs_by_tag"

    async def get_songs(self, db: Session, tags: List[str], skip: int = 0, limit: int = 100, current_user: Optional[schemas.User] = None):
        songs = db.query(models.Song).\
            filter(models.Song.tags.any(models.Tag.name.in_(tags))).\
            offset(skip).\
            limit(limit).\
            all()
        if current_user:
            current_db_user = db.query(models.User).filter(models.User.username == current_user.username).first()
            add_like_attr(current_db_user, songs)
        return songs

crud_tag = TagCRUD()
