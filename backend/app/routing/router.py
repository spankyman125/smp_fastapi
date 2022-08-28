from fastapi import APIRouter

from .endpoints import artist, test, song, album, user, auth, queue, playlist, search, tags, home

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router        ,tags=["auth"]              ,prefix="/auth"    )
api_router.include_router(artist.router      ,tags=["artists"]           ,prefix="/artists" )
api_router.include_router(song.router        ,tags=["songs"]             ,prefix="/songs"   )
api_router.include_router(album.router       ,tags=["albums"]            ,prefix="/albums"  )
 
api_router.include_router(user.router        ,tags=["users"]             ,prefix="/users"   )
api_router.include_router(user.router_me     ,tags=["users/me"]          ,prefix="/users"   )
api_router.include_router(user.router_others ,tags=["users/{username}"]  ,prefix="/users"   )
api_router.include_router(queue.router       ,tags=["users/me/queue"]    ,prefix="/users/me/queue"   )
api_router.include_router(playlist.router    ,tags=["users/me/playlists"],prefix="/users/me/playlists"   )
api_router.include_router(search.router      ,tags=["search"]            ,prefix="/search"    )
api_router.include_router(tags.router        ,tags=["tags"]              ,prefix="/tags"    )
api_router.include_router(home.router        ,tags=["home"]              ,prefix="/home"    )

api_router.include_router(test.router        ,tags=["test"]             ,prefix="/test"    )
# api_router.include_router(stream.router      ,tags=["stream"])