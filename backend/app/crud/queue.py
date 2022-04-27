from app import models
from sqlalchemy.orm import joinedload
from fastapi import HTTPException


class QueueCRUD():
    def __init__(self):
        pass

    def get(self, db, user: models.User):
        queue = db.query(models.Song).\
            filter(models.Song.id.in_(user.queue.songs)).\
            options(joinedload(models.Song.album)).\
            options(joinedload(models.Song.artists))
        id_map = {t.id: t for t in queue}
        songs = [id_map[n] for n in user.queue.songs]
        result = {
            "current_position": user.queue.current_position,
            "songs": songs 
        }
        return result

    def add(self, db, user: models.User, id: int):
        if bool(db.query(models.Song.id).filter_by(id=id).first()):            
            if user.queue.current_position == -1:
                user.queue.current_position += 1
            user.queue.songs = user.queue.songs + [id]
            db.commit()
            db.flush()
            return user.queue # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='Wrong song id')

    def delete(self, db, user: models.User, position: int):
        if user.queue.current_position == -1:
            raise HTTPException(status_code=400, detail='Queue is empty')
        queue = user.queue.songs.copy()
        if len(queue) > position:
            if (position == user.queue.current_position):
                    user.queue.current_position -= 1
            if (position == 0 and len(queue) > 1):
                    user.queue.current_position = 0
            queue.pop(position)
            user.queue.songs = queue
            db.commit()
            return user.queue # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='Wrong position')

    def clear(self, db, user: models.User):
        user.queue.songs = []
        user.queue.current_position = -1
        db.commit()
        return user.queue # возвращать только подтверждение?

    def current(self, db, user: models.User):
        if user.queue.current_position != -1:
            current_song = db.query(models.Song).\
                filter_by(id=user.queue.songs[user.queue.current_position]).\
                options(joinedload(models.Song.album)).\
                options(joinedload(models.Song.artists)).\
                first()
            return current_song # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='Queue is empty')

    def next(self, db, user: models.User):
        if user.queue.current_position == -1:
            raise HTTPException(status_code=400, detail='Queue is empty')
        if user.queue.current_position < len(user.queue.songs) - 1:
            user.queue.current_position += 1
            db.commit()
            current_song = db.query(models.Song).\
                filter_by(id=user.queue.songs[user.queue.current_position]).\
                options(joinedload(models.Song.album)).\
                options(joinedload(models.Song.artists)).\
                first()
            return current_song # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='No next track')

    def prev(self, db, user: models.User):
        if user.queue.current_position == -1:
            raise HTTPException(status_code=400, detail='Queue is empty')
        if user.queue.current_position > 0:
            user.queue.current_position -= 1
            db.commit()
            current_song = db.query(models.Song).\
                filter_by(id=user.queue.songs[user.queue.current_position]).\
                options(joinedload(models.Song.album)).\
                options(joinedload(models.Song.artists)).\
                first()
            return current_song # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='No previous track')

    def replace(self, db, user: models.User, song_list):
        check = db.query(models.Song).\
            filter(models.Song.id.in_(song_list))
        id_map = {t.id: t for t in check}
        try:
            list = [id_map[n] for n in song_list]
            user.queue.songs = song_list
            user.queue.current_position = 0
            db.commit()
        except:
            raise HTTPException(status_code=400, detail='Wrong id provided')
        return self.get(db, user)
crud_queue = QueueCRUD()