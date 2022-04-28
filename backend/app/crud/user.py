from sqlalchemy.orm import Session, joinedload
import os, uuid
from fastapi import UploadFile, File
from app import main
from app import models, schemas
from app.security import get_password_hash, verify_password

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    password_hash = get_password_hash(user.password)
    db_user = models.User(password_hash=password_hash, username=user.username)
    db.add(db_user)
    db.flush()
    db.refresh(db_user)
    db_queue = models.Queue(user_id=db_user.id, songs=[], current_position=-1)
    db.add(db_queue)
    db.commit()
    return db_user

def update_user(db: Session, user:schemas.UserReturn, user_about: schemas.UserAbout):
    db_user = db.query(models.User).filter_by(id=user.id).first()
    db_user.name=user_about.name
    db_user.surname=user_about.surname
    db_user.about=user_about.about
    db_user.email=user_about.email
    db.commit()
    db.flush()
    db.refresh(db_user)
    return db_user

async def update_user_avatar(db: Session, user:schemas.UserReturn, file: UploadFile=File(...)):
    file.filename = f"{uuid.uuid4()}.png"
    path = f"/static/images/user_avatars/{file.filename}"
    contents = await file.read()
    with open(f"{main.APP_PATH}{path}", "wb") as f:
        f.write(contents)
    
    db_user = db.query(models.User).filter_by(id=user.id).first()
    if db_user.image_url!="/static/images/user_avatars/default.png" and os.path.isfile(f"{main.APP_PATH}{db_user.image_url}"):
        os.remove(f"{main.APP_PATH}{db_user.image_url}")
    db_user.image_url=path
    db.commit()
    db.flush()
    db.refresh(db_user)
    return db_user

def authenticate_user(username: str, password: str, db: Session):
    user = get_user(db, username) 
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user