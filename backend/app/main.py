import os
from typing import List, Optional
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas, filldata
from .database import engine

app = FastAPI()
app.mount("/static/images", StaticFiles(directory="app/static/images"), name="static_images")
app.mount("/static/css", StaticFiles(directory="app/static/css"), name="static_css")
app.mount("/static/js", StaticFiles(directory="app/static/js"), name="static_js")

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/songs/{id}", response_model=schemas.SongRead, tags=["song"])
def read_song(id: int, db: Session = Depends(get_db)):
    song = crud.get_song(db, song_id=id)
    if song is None:
        raise HTTPException(status_code=404, detail='Song not found')
    return song

@app.get("/songs/", response_model=List[schemas.SongRead], tags=["song"])
def read_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    songs = crud.get_songs(db, skip=skip, limit=limit)
    return songs

@app.get("/albums/{id}", response_model=schemas.AlbumRead, tags=["album"])
def read_album(id: int, db: Session = Depends(get_db)):
    album = crud.get_album(db, album_id=id)
    if album is None:
        raise HTTPException(status_code=404, detail='Album not found')
    return album

@app.get("/albums/", response_model=List[schemas.AlbumRead], tags=["album"])
def read_songs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    songs = crud.get_albums(db, skip=skip, limit=limit)
    return songs

@app.get("/artists/{id}", response_model=schemas.ArtistRead, tags=["artist"])
def read_artist(id: int, db: Session = Depends(get_db)):
    artist = crud.get_artist(db, artist_id=id)
    if artist is None:
        raise HTTPException(status_code=404, detail='Artist not found')
    return artist

@app.get("/artists/", response_model=List[schemas.ArtistRead], tags=["artist"])
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    artists = crud.get_artists(db, skip=skip, limit=limit)
    return artists

@app.get("/", tags=["test"])
async def root():
	return {"test":"test"}

@app.get("/filldata/", tags=["test"])
def fill_with_test_data(db: Session = Depends(get_db)):
    filldata.fill_testdata(db)
    return True

CONTENT_CHUNK_SIZE = 100*1024

def get_file(name:str):
    f = open("/container/app/static/songs/" + name,'rb')
    return f, os.path.getsize("/container/app/static/songs/" + name)

def chunk_generator(stream, chunk_size, start, size):
    bytes_read = 0
    stream.seek(start)
    while bytes_read < size:
        bytes_to_read = min(chunk_size,size - bytes_read)
        yield stream.read(bytes_to_read)
        bytes_read = bytes_read + bytes_to_read
    stream.close()

@app.get("/static/songs/{name}", tags=["test"])
async def stream(name:str,range: Optional[str] = Header(None)):

    asked = range or "bytes=0-"
    stream,total_size = get_file(name)
    start_byte = int(asked.split("=")[-1].split('-')[0])

    return StreamingResponse(
        chunk_generator(
            stream,
            start=start_byte,
            chunk_size=CONTENT_CHUNK_SIZE,
            size=total_size
        )
        ,headers={
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start_byte}-{start_byte+CONTENT_CHUNK_SIZE}/{total_size}",
            "Content-Type": "audio/mpeg"
        },
        status_code=206)