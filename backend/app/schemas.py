import datetime
from typing import List, Optional
from pydantic import BaseModel


class SongBase(BaseModel):
    id: int
    title: str
    duration: datetime.timedelta
    file_url: str
    cover_url: str
    liked: Optional[bool]
    class Config:
        orm_mode = True

class AlbumBase(BaseModel):
    id: int
    title: str
    release_date: datetime.date
    cover_url: str
    liked: Optional[bool]

    class Config:
        orm_mode = True

class ArtistBase(BaseModel):
    id: int
    name: str
    cover_url: str
    liked: Optional[bool]
    class Config:
        orm_mode = True

class SongRead(SongBase):
    album: AlbumBase
    artists: List[ArtistBase]

class AlbumRead(AlbumBase):
    songs: List[SongBase]
    artists: List[ArtistBase]

class ArtistRead(ArtistBase):
    albums: List[AlbumBase]
    songs: List[SongBase]

class UserReturn(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class User(BaseModel):
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

class UserCreate(User):
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
    songs: List[SongBase]
    class Config:
        orm_mode = True
class PlaylistAll(BaseModel):
    id: int
    name: str
    cover_url: str
    songs: List[SongBase]
    class Config:
        orm_mode = True

class PlaylistBase(BaseModel):
    id: int
    name: str
    cover_url: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None