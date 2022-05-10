import uuid, os
from calendar import c
from app import models, main, schemas
from sqlalchemy.orm import joinedload, Session
from fastapi import HTTPException, UploadFile, File
from typing import List
from app.crud.song import add_like_attr

class PlaylistCRUD():
    def __init__(self):
        pass

    def create(self, db, user:schemas.User, name: str):
        playlist = models.Playlist(name=name, user_id=user.id, songs=[])
        db.add(playlist)
        db.commit()
        db.refresh(playlist)
        return playlist

    def get(self, db, user:schemas.User, id:int):
        playlist = db.query(models.Playlist).filter_by(id=id).first()
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        if playlist and playlist.user_id == user.id:
            if playlist.songs:
                playlist_joined = db.query(models.Song).\
                    filter(models.Song.id.in_(playlist.songs)).\
                    options(joinedload(models.Song.album)).\
                    options(joinedload(models.Song.artists))
                id_map = {t.id: t for t in playlist_joined}
                songs = [id_map[n] for n in playlist.songs]
                add_like_attr(db_user, songs)
                result = {
                    "id": playlist.id,
                    "name": playlist.name,
                    "cover_url": playlist.cover_url,
                    "songs": songs 
                }
                return result
            else:
                return playlist
        else:
            raise HTTPException(status_code=404, detail='Playlist not found')

    def get_all(self, db: Session, user:schemas.User):
        db_user = db.query(models.User).filter(models.User.username == user.username).first()
        return db_user.playlists

    async def update_playlist_image(self, db: Session, user:models.User, playlist_id: int, file: UploadFile=File(...)):
        playlist = db.query(models.Playlist).filter_by(id=playlist_id).first()
        if playlist and playlist.user_id == user.id:
            file.filename = f"{uuid.uuid4()}.png"
            path = f"/static/images/playlist_covers/{file.filename}"
            contents = await file.read()
            with open(f"{main.APP_PATH}{path}", "wb") as f:
                f.write(contents)
            
            if playlist.cover_url!="/static/images/playlist_covers/default.png" and os.path.isfile(f"{main.APP_PATH}{playlist.cover_url}"):
                os.remove(f"{main.APP_PATH}{playlist.cover_url}")
            playlist.cover_url=path
            db.commit()
            db.flush()
            db.refresh(playlist)
            return playlist
        else:
            raise HTTPException(status_code=404, detail='Playlist not found')

    def add(self, db, user:schemas.User, song_id: int, playlist_id: int):
        playlist = db.query(models.Playlist).filter_by(id=playlist_id).first()
        if playlist and playlist.user_id == user.id:
            if bool(db.query(models.Song.id).filter_by(id=song_id).first()):            
                playlist.songs = playlist.songs + [song_id]
                db.commit()
                db.flush()
                db.refresh(playlist)
                return playlist
            else:
                raise HTTPException(status_code=400, detail='Wrong song id')
        else:
            raise HTTPException(status_code=404, detail='Playlist not found')

    def add_list(self, db, user:schemas.User, playlist_id: int, song_list: List[int]):    
        playlist = db.query(models.Playlist).filter_by(id=playlist_id).first()
        if playlist and playlist.user_id == user.id:   
            check = db.query(models.Song).\
                filter(models.Song.id.in_(song_list))
            id_map = {t.id: t for t in check}
            try:
                list = [id_map[n] for n in song_list]
                playlist.songs = playlist.songs + song_list
                db.commit()
                db.flush()
                db.refresh(playlist)
                return playlist
            except:
                raise HTTPException(status_code=400, detail='Wrong id provided')
        else:
            raise HTTPException(status_code=404, detail='Playlist not found')
   
   
    def clear(self, db, user: schemas.User, playlist_id: int,):
        playlist = db.query(models.Playlist).filter_by(id=playlist_id).first()
        if playlist and playlist.user_id == user.id:   
            playlist.songs = []
            db.commit()
            db.flush()
            db.refresh(playlist)
            return playlist # возвращать только подтверждение?


    def remove(self, db, user:schemas.User, position: int, playlist_id: int):
        playlist = db.query(models.Playlist).filter_by(id=playlist_id).first()
        if playlist and playlist.user_id == user.id:
            if len(playlist.songs) > position:
                temp = playlist.songs.copy()
                temp.pop(position)
                playlist.songs = temp
                db.commit()
                db.flush()
                db.refresh(playlist)
                return playlist
            else:
                raise HTTPException(status_code=400, detail='Wrong position')
        else:
            raise HTTPException(status_code=404, detail='Playlist not found')

    def delete(self, db, user:schemas.User, playlist_id: int):
        playlist = db.query(models.Playlist).filter_by(id=playlist_id).first()
        if playlist and playlist.user_id == user.id:
            db.delete(playlist)
            db.commit()
            return True
        else:
            raise HTTPException(status_code=404, detail='Playlist not found')


crud_playlist = PlaylistCRUD()