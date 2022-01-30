import datetime
from typing import List, Optional
from pydantic import BaseModel, FilePath

class SongBase(BaseModel):
    id: int
    title: str
    duration: datetime.time
    file_url: FilePath
    cover_url: FilePath


class AlbumBase(BaseModel):
    id: int
    title: str
    release_date: datetime.time
    cover_url: FilePath


class ArtistBase(BaseModel):
    id: int
    name: str
    cover_url: FilePath


class SongRead(SongBase):
    album: int
    artists: List[ArtistBase]

    class Config:
        orm_mode = True


class AlbumRead(AlbumBase):
    songs: List[SongBase]
    artists: List[ArtistBase]

    class Config:
        orm_mode = True

        
class ArtistRead(ArtistBase):
    title: str
    duration: datetime.time

    albums: List[AlbumBase]
    songs: List[SongBase]