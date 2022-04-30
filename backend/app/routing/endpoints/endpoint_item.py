from fastapi import HTTPException
from app.crud.song import crud_song
from app.crud.artist import crud_artist
from app.crud.album import crud_album

class EndpointItem:
    def __init__(self, crud_model):
        self.crud_model = crud_model
    
    def read(self, db, id, user):
        item = self.crud_model.get(db, id, user)
        if item is None:
            raise HTTPException(status_code=404, detail='Item not found')
        return item
    
    def like(self, db, id, user):
        item = self.crud_model.get(db, id)
        if item is None:
            raise HTTPException(status_code=404, detail='Item not found')
        like = self.crud_model.like(db, id, user=user)
        return like

    def read_all(self, db, skip, limit, user):
        items = self.crud_model.get_all(db, skip, limit, user)
        return items

song_endpoint = EndpointItem(crud_song)
album_endpoint = EndpointItem(crud_album)
artist_endpoint = EndpointItem(crud_artist)