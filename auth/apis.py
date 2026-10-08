from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

from auth.schemas import Token
from engine.engine import get_db
from auth.service import AuthService as service
from user.schemas import User, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])
session = Depends(get_db)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session=session):
    credentials_error = HTTPException(
        status_code = 401,
        detail = "Invalid or expired token",
        headers = {"WWW-Authenticate": "Bearer"}
    )
    try:
        user = service(db).get_user_from_token(token)
    except jwt.InvalidTokenError:
        raise credentials_error
    if user is None:
        raise credentials_error
    return user

# LOGIN

@router.post("/login", response_model = Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = session):
    user = service(db).authenticate(form.username, form.password)
    if user is None: 
        raise HTTPException(status_code= 401, detail= "incorrect username or password", headers = {"WWWW-Authenticate": "Bearer"})
    return Token(access_token= service(db).create_access_token(user))

@router.get("/me", response_model = UserOut)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
