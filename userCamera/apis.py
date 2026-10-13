from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from engine.engine import get_db
from userCamera.schemas import userCameraUpdate, userCamera, userCameraCreate, userCameraOut
from userCamera.service import userCameraService as service
from camera.schemas import CameraOut
from user.schemas import User
from auth.service import ADMIN, MANAGER

from auth.apis import get_current_user, require_admin_or_manager, require_self_or_admin_or_manager, role_name

router = APIRouter(prefix="/userCameras", tags=["userCameras"])
session = Depends(get_db)

# READ all cameras associated with a user
@router.get("", response_model=list[CameraOut])
async def read_userCameras(user_id: int, db: Session = session,
                           _: User = Depends(require_self_or_admin_or_manager)):
    return service(db).get_userCamerasByUserId(user_id)

# READ all user-camera associations
@router.get("/associations", response_model=list[userCameraOut])
async def read_userCameraAssociations(
    db: Session = session,
    _: User = Depends(require_admin_or_manager),
):
    return service(db).get_userCameras()

# CREATE
@router.post("", response_model = userCameraCreate)
async def create_userCamera(payload: userCameraCreate, db: Session = session,
                            _: userCamera = Depends(require_admin_or_manager)):
    try:
        return service(db).create_userCamera(payload)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="database error while creating user-camera")

# UPDATE
@router.put("{userCamera_id}", response_model=userCameraOut)
async def update_userCamera(userCamera_id: int, payload: userCameraUpdate, db: Session = session,
                            _: userCamera = Depends(require_admin_or_manager)):
    try: 
        user_camera = service(db).update_userCamera(userCamera_id, payload)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while updating")
    if user_camera is None: 
        raise HTTPException(status_code=404, detail="User not found")
    return user_camera

# DELETE 
@router.delete("/{userCamera_id}")
async def delete_userCamera(userCamera_id:int, db: Session = session,
                            _: userCamera = Depends(require_admin_or_manager)):
    try: 
        user_camera = service(db).delete_userCamera(userCamera_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while deleting")
    if user_camera is None:
        raise HTTPException(status_code=404, detail="User not found")
    return{"detail": f"User {userCamera_id} deleted"}