from fastapi import FastAPI
from datetime import timedelta, datetime
import os
from typing import List, Optional
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from . import crud
from . import models
from . import schemas
from . import filldata
from .database import engine

# # Auth, hash etc
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi import status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app = FastAPI()
app.mount("/static/images", StaticFiles(directory="app/static/images"), name="static_images")
app.mount("/static/css", StaticFiles(directory="app/static/css"), name="static_css")
app.mount("/static/js", StaticFiles(directory="app/static/js"), name="static_js")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "5186b05a370027141d3f1e9c19a83aa82b21176e3e1d70641200450fbb964821" #NOT SECRET ;)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str, db: Session):
    user = crud.get_user(db, username) 
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(Depends(get_db), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post("/token", response_model=schemas.Token, tags=["token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/{username}", tags=["test"])
@app.get("/users/{username}", response_model=schemas.UserAll, tags=["user"])
def read_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user(db, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# @app.post("/users/", tags=["user"])
@app.post("/users/", response_model=schemas.UserAll, tags=["user"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user, pwd_context=pwd_context)

@app.get("/auth/test/", tags=["test"])
def auth_test(token: str = Depends(oauth2_scheme)):
    return {"token":token}

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