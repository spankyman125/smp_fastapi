import datetime
from typing import List, Optional
from pydantic import BaseModel, FileUrl

class SongBase(BaseModel):
    id: int
    title: str
    duration: datetime.time
    # file_url: FileUrl
    # cover_url: FileUrl


class AlbumBase(BaseModel):
    id: int
    title: str
    release_date: datetime.date
    cover_url: str


class ArtistBase(BaseModel):
    id: int
    name: str
    # cover_url: FileUrl


class SongRead(SongBase):
    album: AlbumBase
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