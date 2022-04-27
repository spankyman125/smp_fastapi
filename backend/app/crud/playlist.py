from calendar import c
from app import models
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from typing import List

class PlaylistCRUD():
    def __init__(self):
        pass

    def create(self, db, user: models.User, name: str):
        playlist = models.Playlist(name=name, user_id=user.id, songs=[])
        db.add(playlist)
        db.commit()
        db.refresh(playlist)
        return playlist

    def get(self, db, user: models.User, id:int):
        playlist = db.query(models.Playlist).filter_by(id=id).first()
        if playlist and playlist.user_id == user.id:
            if playlist.songs:
                playlist_joined = db.query(models.Song).\
                    filter(models.Song.id.in_(playlist.songs)).\
                    options(joinedload(models.Song.album)).\
                    options(joinedload(models.Song.artists))
                id_map = {t.id: t for t in playlist_joined}
                songs = [id_map[n] for n in playlist.songs]
                result = [{
                    "id": playlist.id,
                    "name": playlist.name,
                    "songs": songs 
                }]
                return result
            else:
                return playlist
        else:
            raise HTTPException(status_code=404, detail='Playlist not found')

    def get_all(self, user: models.User):
        return user.playlists

    def add(self, db, user: models.User, song_id: int, playlist_id: int):
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

    def add_list(self, db, user: models.User, playlist_id: int, song_list: List[int]):    
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

    def remove(self, db, user: models.User, position: int, playlist_id: int):
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

    def delete(self, db, user: models.User, playlist_id: int):
        playlist = db.query(models.Playlist).filter_by(id=playlist_id).first()
        if playlist and playlist.user_id == user.id:
            db.delete(playlist)
            db.commit()
            return True
        else:
            raise HTTPException(status_code=404, detail='Playlist not found')


crud_playlist = PlaylistCRUD()