from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from engine.engine import get_connection, get_db
from user.schemas import User, UserCreate, UserOut, UserUpdate
from user.service import UserService as service

router = APIRouter(prefix="/users", tags=["Users"])
session =  Depends(get_db)

# READ all users
@router.get("", response_model=list[UserOut])
async def read_users(db: Session = session):
    #db = next(get_db())
    return service(db).get_users()

# READ one user
@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db:Session = session):
    user = service(db).get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CREATE
@router.post("", response_model=UserOut)
async def create_user(payload: UserCreate, db: Session = session):
    try:
        return service(db).create_user(payload)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while creating user")

# UPDATE
@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, payload: UserUpdate, db: Session = session):
    try:
        user = service(db).update_user(user_id, payload)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while updating user")
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    return user

# DELETE

@router.delete("/{user_id}")
async def delete_user(user_id:int, db: Session = session):
    try:
        user = service(db).delete_user(user_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while deleting user")
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    return{"detail": f"User {user_id} deleted"}