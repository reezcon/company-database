from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from engine.engine import get_connection, get_db
from user.schemas import User, UserCreate, UserOut, UserUpdate
from user.service import UserService as service

from auth.apis import get_current_user 
from auth.apis import (get_current_user, require_admin,
                       require_admin_or_manager, require_self_or_admin,
                       require_self_or_admin_or_manager)

router = APIRouter(prefix="/users", tags=["Users"])
session =  Depends(get_db)

# READ all users
@router.get("", response_model=list[UserOut])
async def read_users(db: Session = session,
                     _: User = Depends(require_admin_or_manager)):
    return service(db).get_users()

# READ one user
@router.get("/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db:Session = session,
                    _:User = Depends(require_self_or_admin_or_manager)):
    user = service(db).get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CREATE
@router.post("", response_model=UserOut)
async def create_user(payload: UserCreate, db: Session = session,
                      _: User = Depends(require_admin)):
    try:
        return service(db).create_user(payload)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while creating user")

# UPDATE
@router.put("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, payload: UserUpdate, db: Session = session,
                      _: User = Depends(require_self_or_admin)):
    try:
        user = service(db).update_user(user_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while updating user")
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    return user

# DELETE

@router.delete("/{user_id}")
async def delete_user(user_id:int, db: Session = session,
                      _: User = Depends(require_admin)):
    try:
        user = service(db).delete_user(user_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while deleting user")
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    return{"detail": f"User {user_id} deleted"}