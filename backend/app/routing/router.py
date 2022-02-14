from fastapi import APIRouter

from .endpoints import artist, test, stream, song, album, user, auth

api_router = APIRouter()

api_router.include_router(auth.router   ,tags=["auth"]      ,prefix="/auth"    )
api_router.include_router(artist.router ,tags=["artists"]   ,prefix="/artists" )
api_router.include_router(song.router   ,tags=["songs"]     ,prefix="/songs"   )
api_router.include_router(album.router  ,tags=["albums"]    ,prefix="/albums"  )
api_router.include_router(user.router   ,tags=["users"]     ,prefix="/users"   )
api_router.include_router(user.router_me   ,tags=["users/me"]     ,prefix="/users"   )
api_router.include_router(user.router_others   ,tags=["users/{username}"]     ,prefix="/users"   )

api_router.include_router(stream.router ,tags=["stream"])
api_router.include_router(test.router   ,tags=["test"]      ,prefix="/test"    )