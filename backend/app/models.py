from tkinter.tix import INTEGER
import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Table
from sqlalchemy.orm import relationship

from .database import Base

# metadata = sqlalchemy.MetaData()

# SongArtistRelation = Table("SongArtistRelation", Base.metadata,
#     Column("song_id", ForeignKey("songs.id")), # index?
#     Column("artist_id", ForeignKey("artists.id"))
# )

# AlbumArtistRelation = Table("AlbumArtistRelation", Base.metadata,
#     Column("album_id", ForeignKey("albums.id")),
#     Column("artist_id", ForeignKey("artists.id"))
# )


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


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cover_url = Column(String) #/static/images/artist_covers/

    songs = relationship("Song", secondary="song_artist", back_populates="artists")
    albums = relationship("Album", secondary="album_artist", back_populates="artists")


class SongArtistRelation(Base):
    __tablename__ = "song_artist"

    song_id = Column(Integer, ForeignKey("songs.id"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)


class AlbumArtistRelation(Base):
    __tablename__ = "album_artist"

    album_id = Column(Integer, ForeignKey("albums.id"), primary_key=True)
    artist_id = Column(Integer, ForeignKey("artists.id"), primary_key=True)