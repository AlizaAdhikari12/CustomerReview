import os
from datetime import datetime,timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(
    schemes = ['bcrypt'],deprecated='auto'
)
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(password:str , hash_password:str):
    return pwd_context.verify(password,hash_password)

def create_access_token(data : dict, hours : int = 8):
    payload = data.copy()
    payload['exp'] = datetime.utcnow() + timedelta(hours = hours)
    return jwt.encode(payload,SECRET_KEY, algorithm = ALGORITHM)


