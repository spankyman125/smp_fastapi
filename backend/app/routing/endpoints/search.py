import datetime

from fastapi import APIRouter, Depends, Query
from app import main, dependencies, schemas
from typing import List, Optional
from sqlalchemy.orm import joinedload, Session
from app.crud.song import crud_song 
from app.crud.album import crud_album
from app.crud.artist import  crud_artist

router = APIRouter()

@router.get("/artists", response_model=List[schemas.ArtistLoaded], include_in_schema=False)
@router.get("/artists/", response_model=List[schemas.ArtistLoaded])
async def search_artists(
    name: str,
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user_optional),
    limit: Optional[int]=10
):
    result = await main.es_client.search(
        index="artists",
        body= {
            "query":  {
                "bool": {
                    "must": {
                        "match": {
                            "name":name
                        }
                    }
                }
            }
        },
        filter_path="hits.hits._id",
        size=limit
    )
    if result:
        ids=[]
        for hit in result["hits"]["hits"]:
            ids.append(int(hit["_id"]))
        return await crud_artist.get_list(db=db, id_list=ids, current_user=current_user)
    else:
        return []

@router.get("/albums", response_model=List[schemas.AlbumLoaded], include_in_schema=False)
@router.get("/albums/", response_model=List[schemas.AlbumLoaded])
async def search_albums(
    name: str,
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user_optional),
    release_date_from: Optional[datetime.date]=None,
    release_date_to: Optional[datetime.date]=None,
    limit: Optional[int]=10
):
    result = await main.es_client.search(
        index="albums",
        body= {
            "query":  {
                "bool": {
                    "filter": {
                        "range": {
                            "release_date": {
                                "gte": release_date_from,
                                "lte": release_date_to
                            }
                        }
                    },
                    "must": {
                        "match": {
                            "title":name
                        }
                    },
                    "should": { 
                        "match": { "artists": name } 
                    },
                }
            }
        },
        filter_path="hits.hits._id",
        size=limit)
    if result:
        ids=[]
        for hit in result["hits"]["hits"]:
            ids.append(int(hit["_id"]))
        return await crud_album.get_list(db=db, id_list=ids, current_user=current_user)
    else:
        return []

@router.get("/songs", response_model=List[schemas.SongLoaded], include_in_schema=False)
@router.get("/songs/", response_model=List[schemas.SongLoaded])
async def search_songs(
    name: str,
    db: Session = Depends(dependencies.get_db),
    current_user: schemas.User = Depends(dependencies.get_current_user_optional),
    duration_from: Optional[int]=None,
    duration_to: Optional[int]=None,
    tags: Optional[List[str]]=Query([]),
    limit: Optional[int]=10
):
    result =  await main.es_client.search(
        index="songs",
        body= {
            "query":  {
                "bool": {
                    "filter": 
                        (({"range": {"duration": {"gte": duration_from,"lte": duration_to,"format":"epoch_second"}}},
                        {"terms": {"tags":tags}}) 
                        if tags else
                        ({"range": {"duration": { "gte": duration_from,"lte": duration_to,"format":"epoch_second"}}})),
                    "must": {
                        "match": { "title":name }
                    },
                    "should": [
                        { "match": { "album":name } },
                        { "match": { "artists":name } },
                    ]
                }
            }
        },
        filter_path="hits.hits._id",
        size=limit)
    if result:
        ids=[]
        for hit in result["hits"]["hits"]:
            ids.append(int(hit["_id"]))
        return await crud_song.get_list(db=db, id_list=ids, current_user=current_user)
    else:
        return []