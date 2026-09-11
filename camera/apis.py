from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from engine.engine import get_db
from camera.schemas import Camera, CameraCreate, CameraOut, CameraUpdate
from camera.service import CameraService as service

router = APIRouter(prefix="/cameras", tags=["Cameras"])
session = Depends(get_db)

# READ all cameras
@router.get("", response_model = list[CameraOut])
async def read_cameras(db: Session=session):
    return service(db).get_cameras()

# READ one camera
@router.get("/{camera_id}")
async def read_camera(camera_id:int, db: Session=session):
    camera = service(db).get_camera(camera_id)
    if camera is None:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera

# CREATE
@router.post("", response_model=CameraOut)
async def create_camera(payload: CameraCreate, db: Session = session):
    return service(db).create_camera(payload)

# UPDATE
@router.put("/{camera_id}", response_model=CameraOut)
async def update_camera(camera_id: int, payload: CameraUpdate, db: Session = session):
    camera = service(db).update_camera(camera_id, payload)
    if camera is None:
        raise HTTPException (status_code=404, detail = "Camera not found")
    return camera
    
# DELETE
@router.delete("/{camera_id}")
async def delete_camera(camera_id:int, db: Session = session):
    camera = service(db).delete_camera(camera_id)
    if camera is None: 
        raise HTTPException(status_code=404, detail="Camera not found")
    return {"detail": f"Camera {camera_id} is deleted"}
