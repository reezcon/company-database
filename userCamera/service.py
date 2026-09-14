from sqlalchemy.orm import Session 
from sqlalchemy.exc import SQLAlchemyError
from userCamera.schemas import userCamera, userCameraCreate, userCameraUpdate

class userCameraService:
    def __init__(self, db: Session):
        self.db = db

    def get_userCameras(self):
        return self.db.query(userCamera).all()

    def get_userCamera(self, userCamera_id: int):
        return self.db.get(userCamera, userCamera_id)

    def create_userCamera(self, payload: userCameraCreate):
        data = payload.model_dump()
        user_camera = userCamera(**data)
        try: 
            self.db.add(user_camera)
            self.db.commit()
            self.db.refresh(user_camera)
            return user_camera
        except SQLAlchemyError: 
            self.db.rollback()
            raise

    def update_userCamera(self, userCamera_id: int, payload: userCameraUpdate):
        user_camera = self.db.get(userCamera, userCamera_id)
        if user_camera is None: 
            return None 
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items(): 
            setattr(user_camera, field, value)
        try: 
            self.db.commit()
            self.db.refresh(user_camera)
            return user_camera
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_userCamera(self, userCamera_id: int):
        user_camera = self.db.get(userCamera, userCamera_id)
        if user_camera is None:
            return None
        try:
            self.db.delete(user_camera)
            self.db.commit()
            return user_camera
        except SQLAlchemyError:
            self.db.rollback()
            raise
            
