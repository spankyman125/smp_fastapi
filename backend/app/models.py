from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    disabled = Column(Boolean, default=False)
    #avatar 

    artists = relationship("Artist", secondary="user_artist", back_populates="users")
    songs = relationship("Song", secondary="user_song", back_populates="users")
    albums = relationship("Album", secondary="user_album", back_populates="users")
    playlists = relationship("Playlist", back_populates="user")
    queue = relationship("Queue", uselist=False, back_populates="user")


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    duration = Column(Time(timezone=False)) # 2:18
    file_url = Column(String)  # /static/songs/{id}
    cover_url = Column(String) # /static/images/song_covers/ (ссылаться на альбом если нету?, или сингл=альбом)
    
    album_id = Column(Integer, ForeignKey("albums.id"))

    album = relationship("Album", back_populates="songs")
    artists = relationship("Artist", secondary="song_artist", back_populates="songs")
    users = relationship("User", secondary="user_song", back_populates="songs")


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    release_date = Column(Date)
    cover_url = Column(String) # /static/images/album_covers/
    # is_single = Column(Boolean) 

    #jenre relationship fk
    songs = relationship("Song", back_populates="album")
    artists = relationship("Artist", secondary="album_artist", back_populates="albums")
    users = relationship("User", secondary="user_album", back_populates="albums")


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cover_url = Column(String) #/static/images/artist_covers/

    songs = relationship("Song", secondary="song_artist", back_populates="artists")
    albums = relationship("Album", secondary="album_artist", back_populates="artists")
    users = relationship("User", secondary="user_artist", back_populates="artists")

class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True)
    songs = Column(postgresql.ARRAY(Integer))
    current_position = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="queue")

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    songs = Column(postgresql.ARRAY(Integer))
    # cover_url = Column(String) # /static/images/playlist_covers/
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="playlists")

class SongArtistRelation(Base):
    __tablename__ = "song_artist"

    song_id = Column(Integer, ForeignKey("songs.id"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)


class AlbumArtistRelation(Base):
    __tablename__ = "album_artist"

    album_id = Column(Integer, ForeignKey("albums.id"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)


class UserSongLike(Base):
    __tablename__ = "user_song"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    song_id = Column(Integer, ForeignKey("songs.id"), primary_key=True)


class UserAlbumLike(Base):
    __tablename__ = "user_album"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    album_id = Column(Integer, ForeignKey("albums.id"), primary_key=True)


class UserArtistLike(Base):
    __tablename__ = "user_artist"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)
