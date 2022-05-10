from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only
from sqlalchemy.orm import joinedload
from typing import Optional, List
from app import index_conf, security
from app import dependencies, filldata, models, schemas
from app import main
from fastapi.security import OAuth2PasswordRequestForm
from app.crud import user as crud_user

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
    albums = db.query(models.Album).options(load_only("id","title","release_date")).all()
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
    songs = db.query(models.Song).options(load_only("id","title","duration")).options(joinedload(models.Song.tags)).all()
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
            "tags":[tag.name for tag in song.tags]
        })
    return await main.es_client.bulk(operations=operations)