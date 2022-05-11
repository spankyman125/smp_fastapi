import datetime
from typing import List, Optional
from pydantic import BaseModel

class Song(BaseModel):
    id: int
    title: str
    duration: datetime.timedelta
    file_url: str
    cover_url: str
    liked: Optional[bool]
    class Config:
        orm_mode = True

class Album(BaseModel):
    id: int
    title: str
    release_date: datetime.date
    cover_url: str
    liked: Optional[bool]

    class Config:
        orm_mode = True

class Artist(BaseModel):
    id: int
    name: str
    cover_url: str
    liked: Optional[bool]
    class Config:
        orm_mode = True

class Tag(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class SongTagged(Song):
    tags: List[Tag]

class SongLoaded(Song):
    album: Album
    artists: List[Artist]
    tags: List[Tag]

class AlbumLoaded(Album):
    songs: List[SongLoaded]
    artists: List[Artist]

class ArtistLoaded(Artist):
    albums: List[Album]
    songs: List[SongLoaded]

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class UserAll(BaseModel):
    username: str
    image_url: str
    disabled: bool
    name: Optional[str] 
    surname: Optional[str] 
    about: Optional[str] 
    email: Optional[str] 
    class Config:
        orm_mode = True

class UserUpdateImage(User):
    image_url: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserAbout(BaseModel):
    name: Optional[str]
    surname: Optional[str] 
    about: Optional[str] 
    email: Optional[str] 
    class Config:
        orm_mode = True

class Queue(BaseModel):
    current_position: int
    songs: List[int]
    class Config:
        orm_mode = True

class QueueLoaded(Queue):
    songs: List[SongLoaded]

class Playlist(BaseModel):
    id: int
    name: str
    cover_url: str
    songs: Optional[List[int]]
    class Config:
        orm_mode = True

class PlaylistLoaded(Playlist):
    songs: List[SongLoaded]

class PlaylistUpdateImage(Playlist):
    cover_url: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None