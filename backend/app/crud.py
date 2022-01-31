from sqlalchemy.orm import Session, joinedload

from . import models

#Song
def get_song(db: Session, song_id: int):
    return db.query(models.Song).\
        options(joinedload(models.Song.album)).\
        options(joinedload(models.Song.artists)).\
        filter(models.Song.id == song_id).\
        first()

def get_songs(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Song).\
        options(joinedload(models.Song.album)).\
        options(joinedload(models.Song.artists)).\
        offset(skip).\
        limit(limit).\
        all()

#Album
def get_album(db: Session, album_id: int):
    return db.query(models.Album).\
        options(joinedload(models.Album.songs)).\
        options(joinedload(models.Album.artists)).\
        filter(models.Album.id == album_id).\
        first()

def get_albums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Album).\
        options(joinedload(models.Album.songs)).\
        options(joinedload(models.Album.artists)).\
        offset(skip).\
        limit(limit).\
        all()

#Artist
def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).\
        options(joinedload(models.Artist.songs)).\
        options(joinedload(models.Artist.albums)).\
        filter(models.Artist.id == artist_id).\
        first()


def get_artists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artist).\
        options(joinedload(models.Artist.songs)).\
        options(joinedload(models.Artist.albums)).\
        offset(skip).\
        limit(limit).\
        all()

#Test
def fill_testdata(db: Session):
    albums = [
        models.Album(
            title="Album's title",
            release_date="2021-12-10",
            cover_url="/static/images/album_covers/1.png"
        )
    ]
    db.add_all(albums)
    db.commit()

    songs = [
        models.Song(
            title="Song's title",
            duration="2:56",
            file_url="/static/song/1.mp3",
            cover_url="/static/images/song_covers/1.mp3",
            album_id=1
        )
    ]
    artists = [
        models.Artist(
            name="Artist's name", 
            cover_url="/static/images/artist_covers/1.png"
        )
    ]



    db.add_all(songs)
    db.add_all(artists)
    db.commit()

    song_artist = [
        models.SongArtistRelation(song_id=1, artist_id=1)
    ]
    album_artist = [
        models.AlbumArtistRelation(album_id=1, artist_id=1)
    ]
    db.add_all(song_artist)
    db.add_all(album_artist)
    db.commit()

    return True