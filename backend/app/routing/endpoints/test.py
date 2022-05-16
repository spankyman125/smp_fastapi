from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app import index_conf, security
from app import dependencies, filldata, models, schemas
from app import main
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import user as crud_user
import random

router = APIRouter()

@router.post("/get-super-token", response_model=schemas.Token, include_in_schema=False)
@router.post("/get-super-token/", response_model=schemas.Token)
async def get_super_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = crud_user.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    refresh_token = security.create_refresh_token()
    user.refresh_token = refresh_token
    db.commit()
    db.flush()
    access_token = security.create_super_access_token(
        data={"sub": user.username, "type":"access", "id": user.id}
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/filldata")
def root(db: Session = Depends(dependencies.get_db)):
	return filldata.fill_testdata(db)

@router.get("/elastic-info")
async def elastic_info():
	return await main.es_client.info()

@router.get("/get-document/")
async def get_document(id: int, index):
    return await main.es_client.get(index=index, id=id)

@router.get("/delete-all-indexes/")
async def delete_all_indexes():
    await main.es_client.indices.delete(index="albums")
    await main.es_client.indices.delete(index="artists")
    await main.es_client.indices.delete(index="songs")
    return True

@router.get("/create-all-indexes/")
async def create_default_indexes():
    await main.es_client.indices.create(index="albums", settings=index_conf.settings, mappings=index_conf.mappings_albums)
    await main.es_client.indices.create(index="artists",settings=index_conf.settings, mappings=index_conf.mappings_artists)
    await main.es_client.indices.create(index="songs",  settings=index_conf.settings, mappings=index_conf.mappings_songs)
    return True

@router.get("/update-albums-docs/")
async def update_albums_docs(db: Session = Depends(dependencies.get_db)):
    albums = db.query(models.Album).all()
    operations=[]
    for album in albums:
        operations.append({
            'index': {
                "_id":album.id,
                "_index":"albums"
            },
        })
        operations.append({
            "title":album.title,
            "release_date":album.release_date,
            "artists": [artist.name for artist in album.artists]
        })
    return await main.es_client.bulk(operations=operations)

@router.get("/update-artists-docs/")
async def update_artists_docs(db: Session = Depends(dependencies.get_db)):
    artists = db.query(models.Artist).options(load_only("id","name")).all()
    operations=[]
    for artist in artists:
        operations.append({
            'index': {
                "_id":artist.id,
                "_index":"artists"
            },
        })
        operations.append({
            "name":artist.name
        })
    return await main.es_client.bulk(operations=operations)

@router.get("/update-songs-docs/")
async def update_songs_docs(db: Session = Depends(dependencies.get_db)):
    songs = db.query(models.Song).all()
    operations=[]
    for song in songs:
        operations.append({
            'index': {
                "_id":song.id,
                "_index":"songs"
            },
        })
        operations.append({
            "title":song.title,
            "duration":song.duration.total_seconds(),
            "tags":[tag.name for tag in song.tags],
            "album": song.album.title,
            "artists": [artist.name for artist in song.artists],
        })
    return await main.es_client.bulk(operations=operations)


@router.get("/update-pics/")
async def update_pics(db: Session = Depends(dependencies.get_db)):
    albums = db.query(models.Album)
    songs = db.query(models.Song)
    artists = db.query(models.Artist)
    i=0
    for album in albums:
        album.cover_url=f"/static/images/album_covers/{i}.png"
        if i==100:
            i=0
        else:
            i+=1

    for song in songs:
        song.cover_url=f"/static/images/song_covers/{i}.png"
        if i==100:
            i=0
        else:
            i+=1
    
    for artist in artists:
        artist.cover_url=f"/static/images/artist_covers/{i}.png"
        if i==100:
            i=0
        else:
            i+=1
    db.commit()
    # artists = db.query(models.Artist).    
    # songs = db.query(models.Song).    
    pass

@router.get("/random-users-with-album-likes/")
async def random_users(db: Session = Depends(dependencies.get_db)):
    users =[]
    for i in range(1,100):
        users.append(models.User(password_hash=f"pass{i}", username=f"user{i}"))
    db.add_all(users) 
    db.commit()

    user_album=[]
    for user in users:
        random_relations = random.sample(range(1, 100), random.randint(1,20))
        for rel in random_relations:
            user_album.append(
                models.UserAlbumLike(user_id=user.id, album_id=rel)
            )
    db.add_all(user_album)
    db.commit()
    # return await crud_user.update_albums_recomendations(db: Session = Depends(dependencies.get_db))

@router.get("/update-album-recomendations/")
async def update_recomendations(db: Session = Depends(dependencies.get_db)):
    users = db.query(models.User).offset(2).limit(100).all()
    db.query(models.AlbumRelations).delete()
    db.commit()
    for user in users:
        print(f"{user.username}")
        for i in range(len(user.albums)):
            for j in range(i+1,len(user.albums)):
                if i < j:
                    # print(f"{user.albums[i].id}:{user.albums[j].id}")
                    rel = db.query(models.AlbumRelations).get((user.albums[i].id,user.albums[j].id)) 
                    if rel:
                        rel.score = rel.score+1
                        db.commit()
                        db.flush()
                        pass
                    else:
                        db.add(                        
                            models.AlbumRelations(
                                id1=user.albums[i].id,
                                id2=user.albums[j].id,
                                score=1,
                            ))
                        db.commit()
                        db.flush()
                else:
                    # print(f"{user.albums[i].id}:{user.albums[j].id}")
                    rel = db.query(models.AlbumRelations).get((user.albums[j].id,user.albums[i].id)) 
                    if rel:
                        rel.score = rel.score+1
                        db.commit()
                        db.flush()
                        pass
                    else:
                        db.add(                        
                            models.AlbumRelations(
                                id1=user.albums[j].id,
                                id2=user.albums[i].id,
                                score=1,
                            ))
                        db.commit()
                        db.flush()


