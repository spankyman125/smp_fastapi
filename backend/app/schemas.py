import datetime
from faulthandler import disable
from typing import List, Optional
from pydantic import BaseModel

class SongBase(BaseModel):
    id: int
    title: str
    duration: datetime.time
    file_url: str
    cover_url: str
    
    class Config:
        orm_mode = True


class AlbumBase(BaseModel):
    id: int
    title: str
    release_date: datetime.date
    cover_url: str

    class Config:
        orm_mode = True


class ArtistBase(BaseModel):
    id: int
    name: str
    cover_url: str

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

class User(BaseModel):
    username: str
    
class UserAll(BaseModel):
    username: str
    password_hash: str
    disabled: bool
    class Config:
        orm_mode = True

class UserInDB(User):
    password_hash: str

class UserCreate(User):
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None