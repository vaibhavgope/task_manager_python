from datetime import datetime, timedelta
from jose import jwt
from app.config import settings

ALGO = "HS256"

def create_access_token(subject: str | int, role: str):
    expire = datetime.utcnow() + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": str(subject), "role": role, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGO)

def decode_token(token: str):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGO])
