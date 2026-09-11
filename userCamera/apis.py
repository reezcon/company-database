from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from engine.engine import get_db
from userCamera.schemas import userCameraUpdate, userCamera, userCameraCreate, userCameraOut
from userCamera.service import userCameraService as service

router = APIRouter(prefix="/userCameras", tags=["userCameras"])
session = Depends(get_db)

# READ all user-cameras
@router.get("", response_model=list[userCameraOut])
async def read_userCamera(db: Session = session):
    return service(db).get_userCameras()

# READ one user-camera
@router.get("/{userCamera_id}", response_model=userCameraOut)
async def read_userCamera(userCamera_id: int, db: Session = session):
    user_camera = service(db).get_userCamera(userCamera_id)
    if user_camera is None:
        raise HTTPException(status_code=404, detail="User nto found")
    return user_camera

# CREATE
@router.post("", response_model = userCameraCreate)
async def create_userCamera(payload: userCameraCreate, db: Session = session):
    try:
        return service(db).create_userCamera(payload)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="database error while creating user-camera")

# UPDATE
@router.put("{userCamera_id}", response_model=userCameraOut)
async def update_userCamera(userCamera_id: int, payload: userCameraUpdate, db: Session = session):
    try: 
        user_camera = service(db).update_userCamera(userCamera_id, payload)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while updating")
    if user_camera is None: 
        raise HTTPException(status_code=404, detail="User not found")
    return user_camera

# DELETE 
@router.delete("/{userCamera_id}")
async def delete_userCamera(userCamera_id:int, db: Session = session):
    try: 
        user_camera = service(db).delete_userCamera(userCamera_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while deleting")
    if user_camera is None:
        raise HTTPException(status_code=404, detail="User not found")
    return{"detail": f"User {userCamera_id} deleted"}