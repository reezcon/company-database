from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String

from engine.engine import get_connection, Base

engine = get_connection()

class Camera(Base):
    __tablename__ = "cameras"

    camera_id = Column(Integer, primary_key=True, index=True)
    camera_name = Column(String(100), nullable=False, index=True)
    latitude = Column(Integer)
    longitude = Column(Integer)
    region = Column(String(100))
    state = Column(String(50))
    site = Column(String(100))
    rtsp_url = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

class CameraCreate(BaseModel):
    camera_name: str = Field(min_length=2, max_length=100)
    latitude: int
    longitude: int
    region: str = Field(min_length=2, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    site: str = Field(min_length=2, max_length=100)
    rtsp_url: str = Field(min_length=2) 

class CameraOut(BaseModel):
    camera_id: int
    latitude: int
    longitude: int
    region: str
    state: str
    site: str 
    rtsp_url: str 

    class Config:
        orm_mode = True

class CameraUpdate(BaseModel):
    camera_name: str = Field(default = None, min_length=2, max_length=100)
    latitude: int = Field(default = None)
    longitude: int = Field(default = None)
    region: str = Field(default = None, min_length=2, max_length=100)
    state: str = Field(default = None, min_length=2, max_length=100)
    site: str = Field(default = None, min_length=2, max_length=100)
    rtsp_url: str = Field(default = None, min_length=2) 