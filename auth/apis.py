from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import jwt

from auth.schemas import Token
from engine.engine import get_db
from auth.service import AuthService as service
from user.schemas import User, UserOut
from auth.service import ADMIN, MANAGER

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

def role_name(user: User) -> str | None:
    return user.role.name if user.role else None

# Admin only
def require_admin(current_user: User = Depends(get_current_user)):
    if role_name(current_user) != ADMIN:
        raise HTTPException(status_code=403, detail="You do not have permission")
    return current_user

# Admin or manager access
def require_admin_or_manager(current_user: User = Depends(get_current_user)):
    if role_name(current_user) not in (ADMIN, MANAGER):
        raise HTTPException(status_code=403, detail="You do not have permission")
    return current_user

# Own record, or admin
def require_self_or_admin(user_id: int, current_user: User = Depends(get_current_user)):
    if current_user.user_id != user_id and role_name(current_user) != ADMIN:
        raise HTTPException(status_code=403, detail="You do not have permission")
    return current_user

def require_self_or_admin_or_manager(user_id: int, current_user: User=Depends(get_current_user)):
    if current_user.user_id != user_id and role_name(current_user) not in (ADMIN, MANAGER):
        raise HTTPException(status_code=404, detail="You do not have permission")
    return current_user

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
