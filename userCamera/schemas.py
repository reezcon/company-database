from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from engine.engine import Base

from user.schemas import UserOut
from camera.schemas import CameraOut

class userCamera(Base):
    __tablename__ = "user_cameras"
    userCamera_id = Column(Integer, primary_key= True, index = True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.camera_id", ondelete="CASCADE"), nullable=False, index=True)

    user = relationship("User", back_populates="user_cameras")
    camera = relationship("Camera", back_populates="user_cameras")

class userCameraCreate(BaseModel):
    user_id: int 
    camera_id: int

class userCameraUpdate(BaseModel):
    user_id: int | None = None
    camera_id: int | None = None

class userCameraOut(BaseModel):
    user: UserOut
    camera: CameraOut