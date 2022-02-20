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
        result = [{
            "current_position": user.queue.current_position,
            "songs": songs 
        }]
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
        queue = user.queue.songs.copy()
        if len(queue) > position:
            if (position == user.queue.current_position):
                    user.queue.current_position -= 1
            if (position == 0 and len(queue)>1):
                    user.queue.current_position = 0
            queue.pop(position)
            user.queue.songs = queue
            db.commit()
            return user.queue # возвращать только подтверждение?
        else:
            raise HTTPException(status_code=400, detail='Wrong position')

    def replace(self, user: models.User, song_list):
        return user.queue # возвращать только подтверждение?

crud_queue = QueueCRUD()