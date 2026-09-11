from datetime import datetime

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime

from engine.engine import get_connection, Base

engine = get_connection()

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False, index = True)
    description = Column(String(254), nullable=True)
    created_on = Column(DateTime, default=datetime.now)

Base.metadata.create_all(bind=engine)

class RoleCreate(BaseModel):
    role_name: str = Field(min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=255)

class RoleOut(BaseModel):
    role_id: int 
    role_name: str 
    discription: str | None = None

    class Config:
        orm_mode = True

class RoleUpdate(BaseModel):
    role_name: str = Field(min_length=2, max_length=50)
    description: str = Field(default=None, max_length=254) 
