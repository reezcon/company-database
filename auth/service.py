import os 
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError
from sqlalchemy.orm import Session

from user.schemas import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

password_hasher = PasswordHash.recommended()

# Roles
ADMIN = "admin"
MANAGER = "manager"
USER = "user"


def hash_password(password: str) -> str:
    return password_hasher.hash(password)

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate(self, username: str, password: str):
        user = self.db.query(User).filter(User.username == username).first()
        if user is None:
            return None
        try:
            if not password_hasher.verify(password, user.password):
                return None
        except UnknownHashError:
            return None
        return user

    def create_access_token(self, user: User) -> str: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode({"sub": str(user.user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

    def get_user_from_token(self,token: str):
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return self.db.get(User, int(user_id))

    