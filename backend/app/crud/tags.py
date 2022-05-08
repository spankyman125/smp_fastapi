from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from typing import Optional, List

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

    def get_songs(self, db: Session, tags: List[str], skip: int = 0, limit: int = 100):
        songs = db.query(models.Song).\
            options(joinedload(models.Song.tags)).\
            filter(models.Tag.name.in_(tags)).\
            offset(skip).\
            limit(limit).\
            all()
        return songs

crud_tag = TagCRUD()
