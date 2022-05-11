from app import models, schemas
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from typing import List
from app.crud.song import add_like_attr

class QueueCRUD():
    def __init__(self):
        pass

    def get(self, db, user: schemas.User):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        queue = db.query(models.Song).\
            filter(models.Song.id.in_(db_user.queue.songs)).\
            options(selectinload(models.Song.album)).\
            options(selectinload(models.Song.artists))
        id_map = {t.id: t for t in queue}
        songs = [id_map[n] for n in db_user.queue.songs]
        add_like_attr(db_user, songs)

        result = {
            "current_position": db_user.queue.current_position,
            "songs": songs 
        }
        return result

    def add(self, db, user: schemas.User, id: int):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if bool(db.query(models.Song.id).filter_by(id=id).first()):            
            if db_user.queue.current_position == -1:
                db_user.queue.current_position += 1
            db_user.queue.songs = db_user.queue.songs + [id]
            db.commit()
            db.flush()
            return db_user.queue # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='Wrong song id')

    def delete(self, db, user: schemas.User, position: int):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if db_user.queue.current_position == -1:
            raise HTTPException(status_code=400, detail='Queue is empty')
        queue = db_user.queue.songs.copy()
        if len(queue) > position:
            if (position == db_user.queue.current_position):
                    db_user.queue.current_position -= 1
            if (position == 0 and len(queue) > 1):
                    db_user.queue.current_position = 0
            queue.pop(position)
            db_user.queue.songs = queue
            db.commit()
            return db_user.queue # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='Wrong position')

    def clear(self, db, user: schemas.User):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        db_user.queue.songs = []
        db_user.queue.current_position = -1
        db.commit()
        return db_user.queue # возвращать только подтверждение?

    def current(self, db, user: schemas.User):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if db_user.queue.current_position != -1:
            current_song = db.query(models.Song).\
                filter_by(id=db_user.queue.songs[db_user.queue.current_position]).\
                options(selectinload(models.Song.album)).\
                options(selectinload(models.Song.artists)).\
                first()
            add_like_attr(db_user, [current_song])
            return current_song # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='Queue is empty')

    def next(self, db, user: schemas.User):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if db_user.queue.current_position == -1:
            raise HTTPException(status_code=400, detail='Queue is empty')
        if db_user.queue.current_position < len(db_user.queue.songs) - 1:
            db_user.queue.current_position += 1
            db.commit()
            current_song = db.query(models.Song).\
                filter_by(id=db_user.queue.songs[db_user.queue.current_position]).\
                options(selectinload(models.Song.album)).\
                options(selectinload(models.Song.artists)).\
                first()
            add_like_attr(db_user, [current_song])
            return current_song # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='No next track')

    def prev(self, db, user: schemas.User):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if db_user.queue.current_position == -1:
            raise HTTPException(status_code=400, detail='Queue is empty')
        if db_user.queue.current_position > 0:
            db_user.queue.current_position -= 1
            db.commit()
            current_song = db.query(models.Song).\
                filter_by(id=db_user.queue.songs[db_user.queue.current_position]).\
                options(selectinload(models.Song.album)).\
                options(selectinload(models.Song.artists)).\
                first()
            add_like_attr(db_user, [current_song])
            return current_song # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='No previous track')

    def replace(self, db, user: schemas.User, song_list):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        check = db.query(models.Song).\
            filter(models.Song.id.in_(song_list))
        id_map = {t.id: t for t in check}
        try:
            list = [id_map[n] for n in song_list]
            db_user.queue.songs = song_list
            if len(song_list) == 0:
                db_user.queue.current_position = -1
            else:                
                db_user.queue.current_position = 0
            db.commit()
        except:
            raise HTTPException(status_code=400, detail='Wrong id provided')
        return db_user.queue

crud_queue = QueueCRUD()