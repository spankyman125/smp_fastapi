import datetime
import random
import time
from sqlalchemy.orm import Session
from app import main
from . import models

import contextlib
from sqlalchemy import MetaData
from app.database import engine, Base
from app.random_names import artists_random, titles_random, albums_random
meta = MetaData()


def random_date(seed):
    # random.seed(seed)
    d = random.randint(1, int(time.time()))
    return datetime.date.fromtimestamp(d).strftime('%Y-%m-%d')

#Test
def fill_testdata(db: Session):
    
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        con.execute('TRUNCATE {} RESTART IDENTITY;'.format(
            ','.join(table.name 
                    for table in reversed(Base.metadata.sorted_tables))))
        trans.commit()

    albums=[]
    artists=[]
    for i in range(0,10):
        for j in range(0,10):
            albums.append(
                models.Album(
                    title=f"{random.choice(albums_random)} {random.randint(0,999)}",
                    release_date=random_date(random.randint(0,999)),
                    cover_url=f"/static/images/album_covers/{i}.png"
                )
            )
            artists.append(
                models.Artist(
                    name=f"{random.choice(artists_random)} {random.randint(0,999)}",
                    cover_url=f"/static/images/artist_covers/{i}.png"
                )
            )

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

    songs=[]
    for i in range(1,10):
        for j in range(1,10):
            for k in range(1,10):
                songs.append(
                    models.Song(
                        title=f"{random.choice(titles_random)} {random.randint(0,999)}",
                        duration=durations[i-1],
                        file_url=f"/static/songs/{i}.mp3",
                        cover_url=f"/static/images/song_covers/{i}.png",
                        album_id=random.randint(1,100)
                    )
                )

    db.add_all(songs)
    db.add_all(artists)
    db.add_all(albums)
    db.commit()

    tag_names=["rock","metal","pop","indie","hip-hop","jazz","blues"]
    tags=[]
    for tag in tag_names:
        tags.append(
            models.Tag(name=tag)
        )
    db.add_all(tags)
    db.commit()


    song_artists=[]
    for song in songs:
        random_relations = random.sample(range(1, 100), random.randint(1,4))
        for rel in random_relations:
            song_artists.append(
                models.SongArtistRelation(song_id=song.id, artist_id=rel)
            )
    db.add_all(song_artists)
    db.commit()


    song_tags=[]
    for song in songs:
        random_relations = random.sample(range(1, len(tags)-1), random.randint(1, 4))
        for rel in random_relations:
            song_tags.append(
                models.SongTag(song_id=song.id, tag_id=rel)
            )
    db.add_all(song_tags)
    db.commit()

    album_artists=[]
    for album in albums:
        random_relations = random.sample(range(1, 100), random.randint(1, 4))
        for rel in random_relations:
            album_artists.append(
                models.AlbumArtistRelation(album_id=album.id, artist_id=rel)
            )
    db.add_all(album_artists)
    db.commit()

    # album_artists=[]
    # for album in album_artist_relations:
    #     for artist in album_artist_relations[album]:
    #         album_artists.append(
    #             models.AlbumArtistRelation(album_id=album, artist_id=artist)
    #         )

    # db.add_all(album_artists)
    # db.commit()

    return True