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
    random.seed(seed)
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
    # 4 альбома и 4 исполнителей
    for i in range(0,10):
        for j in range(0,10):
            albums.append(
                models.Album(
                    title=f"{random.choice(albums_random)} {i}",
                    release_date=random_date(i),
                    cover_url=f"/static/images/album_covers/{i}.png"
                )
            )
            artists.append(
                models.Artist(
                    name=f"{random.choice(artists_random)} {i}",
                    cover_url=f"/static/images/artist_covers/{i}.png"
                )
            )
    
    db.add_all(artists)
    db.add_all(albums)
    db.commit()


    # albums=[]
    # songs=[]
    # artists=[]
    # song_artists=[]
    # song_tags=[]
    # album_artists=[]
    # tags=["rock","metal","pop","indie","hip-hop","jazz","blues"]
    # tags_models=[]
    # durations=[
    #     "00:02:08",
    #     "00:02:03",
    #     "00:01:57",
    #     "00:01:53",
    #     "00:02:05",
    #     "00:01:50",
    #     "00:01:56",
    #     "00:02:06",
    #     "00:01:53",
    #     "00:01:48",
    # ]

    # album_song_relations = [
    #     1,1,1,2,2,3,3,4,4,4
    # ]
    
    # song_artist_relations = {
    #     1:[1,2,3,4],
    #     2:[2,4],
    #     3:[3,4],
    #     4:[4],
    #     5:[2],
    #     6:[1,2,3,4],
    #     7:[1],
    #     8:[3],
    #     9:[4],
    #     10:[4],
    # }

    # album_artist_relations = {
    #     1:[1,2,3],
    #     2:[1,2],
    #     3:[2,4],
    #     4:[2],
    # }

    # song_tag_relations = {
    #     1:[1,5,4],
    #     2:[2,4],
    #     3:[3,4],
    #     4:[4],
    #     5:[2],
    #     6:[1,2,4],
    #     7:[1,5],
    #     8:[6],
    #     9:[2],
    #     10:[1,4],
    # }


    # # 10 песен
    # for i in range(1,11):
    #     songs.append(
    #         models.Song(
    #             id=i,
    #             title=f"Song's title {i}",
    #             duration=durations[i-1],
    #             file_url=f"/static/songs/{i}.mp3",
    #             cover_url=f"/static/images/song_covers/{i}.png",
    #             album_id=album_song_relations[i-1]
    #         )
    #     )

    # for i in range(1,7):
    #     tags_models.append(
    #         models.Tag(id=i,name=tags[i])
    #     )
    
    # db.add_all(tags_models)

    # db.add_all(songs)
    # db.commit()

    # for song in song_artist_relations:
    #     for artist in song_artist_relations[song]:
    #         song_artists.append(
    #             models.SongArtistRelation(song_id=song, artist_id=artist)
    #         )
    
    # for song in song_tag_relations:
    #     for tag in song_tag_relations[song]:
    #         song_tags.append(
    #             models.SongTag(song_id=song, tag_id=tag)
    #         )

    # for album in album_artist_relations:
    #     for artist in album_artist_relations[album]:
    #         album_artists.append(
    #             models.AlbumArtistRelation(album_id=album, artist_id=artist)
    #         )

    # db.add_all(song_artists)
    # db.add_all(song_tags)
    # db.add_all(album_artists)
    # db.commit()

    return True