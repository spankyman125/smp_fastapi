import datetime
from app import schemas
from typing import List, Optional
from pydantic import BaseModel

class SongLikeRequired(schemas.Song):
    liked: bool

class AlbumLikeRequired(schemas.Album):
    liked: bool

class ArtistLikeRequired(schemas.Artist):
    liked: bool

class SongLoadedLikeRequired(schemas.SongLoaded):
    album: AlbumLikeRequired
    artists: List[ArtistLikeRequired]

class AlbumLoadedLikeRequired(schemas.AlbumLoaded):
    songs: List[SongLoadedLikeRequired]
    artists: List[ArtistLikeRequired]

class ArtistLoadedLikeRequired(schemas.ArtistLoaded):
    albums: List[AlbumLikeRequired]
    songs: List[SongLoadedLikeRequired]

class PlaylistLoadedLikeRequired(schemas.PlaylistLoaded):
    songs: List[SongLikeRequired]

class QueueLikeRequired(schemas.Queue):
    songs: List[SongLikeRequired]

