from sqlalchemy.orm import Session
from camera.schemas import CameraUpdate, CameraOut, CameraCreate, Camera
from sqlalchemy.exc import SQLAlchemyError

class CameraService:
    def __init__(self, db: Session):
        self.db = db 

    def get_cameras(self):
        return self.db.query(Camera).all()

    def get_camera(self, camera_id: int):
        return self.db.get(Camera, camera_id)

    def _check_duplicates(self, camera_name: str =None):
        if camera_name is None:
            return
        query = self.db.query(Camera).filter(Camera.camera_name == camera_name)
        if query.first() is not None: 
            raise ValueError("That camera name already exists")
            

    def create_camera(self, payload: CameraCreate):
        self._check_duplicates(camera_name=payload.camera_name)
        data = payload.model_dump()
        camera = Camera(**data)
        try: 
            self.db.add(camera)
            self.db.commit()
            self.db.refresh(camera)
            return camera
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def update_camera(self, camera_id: int, payload: CameraUpdate):
        camera = self.db.get(Camera, camera_id)
        if camera is None: 
            return None
        updates = payload.model_dump(exclude_unset=True)
        self._check_duplicates(camera_name = updates.get("camera_name"))
        for field, value in updates.items():
            setattr(camera, field, value)
        try: 
            self.db.commit()
            self.db.refresh(camera)
            return camera
        except SQLAlchemyError:
            self.db.rollback()

    def delete_camera(self, camera_id:int):
        camera = self.db.get(Camera, camera_id)
        if camera is None:
            return None
        try: 
            self.db.delete(camera)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
"""
def get_cameras(db: Session):
    return db.query(Camera).all()

def get_camera(db: Session, camera_id: int):
    return db.get(Camera, camera_id)

def create_camera(db: Session, payload: CameraCreate):
    data = payload.model_dump()
    camera = Camera(**data)
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera

def update_camera(db: Session, camera_id: int, payload: CameraUpdate):
    camera = db.get(Camera, camera_id)
    if camera is None:
        return None
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.list():
        setattr(camera, field, value)
    db.commit()
    db.refresh(camera)
    return camera

def delete_camera(db: Session, camera_id):
    camera = db.get(Camera, camera_id)
    if camera is None: 
        return None
    db.delete(camera)
    db.commit()
    return camera"""