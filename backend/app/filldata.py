import datetime
import random
import time
from sqlalchemy.orm import Session

from . import models

def random_date(seed):
    random.seed(seed)
    d = random.randint(1, int(time.time()))
    return datetime.date.fromtimestamp(d).strftime('%Y-%m-%d')

#Test
def fill_testdata(db: Session):
    albums=[]
    songs=[]
    artists=[]
    song_artists=[]
    album_artists=[]

    durations=[
        "00:02:08",
        "00:02:03",
        "00:01:57",
        "00:01:53",
        "00:02:05",
        "00:01:50",
        "00:01:56",
        "00:02:06",
        "00:01:53",
        "00:01:48",
    ]

    album_song_relations = [
        1,1,1,2,2,3,3,4,4,4
    ]
    
    song_artist_relations = {
        1:[1,2,3,4],
        2:[2,4],
        3:[3,4],
        4:[4],
        5:[2],
        6:[1,2,3,4],
        7:[1],
        8:[3],
        9:[4],
        10:[4],
    }

    album_artist_relations = {
        1:[1,2,3],
        2:[1,2],
        3:[2,4],
        4:[2],
    }

    # 4 альбома и 4 исполнителей
    for i in range(1,5):
        albums.append(
            models.Album(
                id=i,
                title=f"Album's title {i}",
                release_date=random_date(i),
                cover_url=f"/static/images/album_covers/{i}.png"
            )
        )
        artists.append(
            models.Artist(
                id=i,
                name=f"Artist's name {i}",
                cover_url=f"/static/images/artist_covers/{i}.png"
            )
        )

    # 10 песен
    for i in range(1,11):
        songs.append(
            models.Song(
                id=i,
                title=f"Song's title {i}",
                duration=durations[i-1],
                file_url=f"/static/songs/{i}.mp3",
                cover_url=f"/static/images/song_covers/{i}.png",
                album_id=album_song_relations[i-1]
            )
        )


    
    db.add_all(albums)
    db.commit()
    db.add_all(songs)
    db.add_all(artists)
    db.commit()

    for song in song_artist_relations:
        for artist in song_artist_relations[song]:
            song_artists.append(
                models.SongArtistRelation(song_id=song, artist_id=artist)
            )

    for album in album_artist_relations:
        for artist in album_artist_relations[album]:
            album_artists.append(
                models.AlbumArtistRelation(album_id=album, artist_id=artist)
            )

    db.add_all(song_artists)
    db.add_all(album_artists)
    db.commit()

    return True