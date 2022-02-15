from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "5186b05a370027141d3f1e9c19a83aa82b21176e3e1d70641200450fbb964821" #NOT SECRET ;)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 240

def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

