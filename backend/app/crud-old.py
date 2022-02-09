# from sqlalchemy.orm import Session, joinedload
# from . import models, schemas
# from app.security import get_password_hash, verify_password

# #Song
# def get_song(db: Session, song_id: int):
#     return db.query(models.Song).\
#         options(joinedload(models.Song.album)).\
#         options(joinedload(models.Song.artists)).\
#         filter(models.Song.id == song_id).\
#         first()

# def get_songs(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Song).\
#         options(joinedload(models.Song.album)).\
#         options(joinedload(models.Song.artists)).\
#         offset(skip).\
#         limit(limit).\
#         all()

#Album
# def get_album(db: Session, album_id: int):
#     return db.query(models.Album).\
#         options(joinedload(models.Album.songs)).\
#         options(joinedload(models.Album.artists)).\
#         filter(models.Album.id == album_id).\
#         first()

# def get_albums(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Album).\
#         options(joinedload(models.Album.songs)).\
#         options(joinedload(models.Album.artists)).\
#         offset(skip).\
#         limit(limit).\
#         all()

#Artist
# def get_artist(db: Session, artist_id: int):
#     return db.query(models.Artist).\
#         options(joinedload(models.Artist.songs)).\
#         options(joinedload(models.Artist.albums)).\
#         filter(models.Artist.id == artist_id).\
#         first()

# def get_artists(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Artist).\
#         options(joinedload(models.Artist.songs)).\
#         options(joinedload(models.Artist.albums)).\
#         offset(skip).\
#         limit(limit).\
#         all()

# def get_artists_liked(db: Session, user: models.User , skip: int = 0, limit: int = 100) :
#     return user.artists

# def like_artist(db: Session, artist_id: int, user: models.User):
#     like = db.query(models.UserArtistLike).get((user.id, artist_id))
#     if like:
#         db.delete(like)
#         db.commit()
#         return False 
#     else:
#         like = models.UserArtistLike(user_id=user.id, artist_id=artist_id)
#         db.add(like)
#         db.commit()
#         db.refresh(like)
#         return True

#Auth
# def get_user(db: Session, username: str):
#     return db.query(models.User).filter(models.User.username == username).first()

# def create_user(db: Session, user: schemas.UserCreate):
#     password_hash = get_password_hash(user.password)
#     db_user = models.User(password_hash=password_hash, username=user.username)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def authenticate_user(username: str, password: str, db: Session):
#     user = get_user(db, username) 
#     if not user:
#         return False
#     if not verify_password(password, user.password_hash):
#         return False
#     return user