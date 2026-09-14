from datetime import datetime
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime

from engine.engine import Base

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, nullable=False, index = True)
    description = Column(String(254), nullable=True)
    created_on = Column(DateTime, default=datetime.now)

    users = relationship("User", back_populates = "role")

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
