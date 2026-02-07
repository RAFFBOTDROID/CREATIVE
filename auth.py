from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET = "CREATIVE_SECRET_KEY"
pwd = CryptContext(schemes=["bcrypt"])

def hash_password(password):
    return pwd.hash(password)

def verify_password(password, hashed):
    return pwd.verify(password, hashed)

def create_token(data):
    expire = datetime.utcnow() + timedelta(days=7)
    return jwt.encode({**data, "exp": expire}, SECRET)
