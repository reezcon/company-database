from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String

from engine.engine import get_connection, Base

engine = get_connection()

class userCamera(Base):
    userCamera_id = Column(Integer, primary_key= True, index = True)
    user_id = Column(Integer, ForeignKey= "user.user_id", nullable=False, index = True)
    camera_id = Column(Integer, ForeignKey="camera.camera_id", nullable=False, index= True)

Base.metadata.create_all(bind=engine)

class userCameraCreate(BaseModel):
    user_id: int 
    camera_id: int

class userCameraUpdate(BaseModel):
    user_id: int | None = None
    camera_id: int | None = None

class userCameraOut(BaseModel):
    user_id: int
    camera_id: int