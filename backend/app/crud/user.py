from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.security import get_password_hash, verify_password

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    password_hash = get_password_hash(user.password)
    db_user = models.User(password_hash=password_hash, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(username: str, password: str, db: Session):
    user = get_user(db, username) 
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user