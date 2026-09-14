from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from engine.engine import get_connection, Base

engine = get_connection()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column("email", String, unique=True, nullable=False)
    phone_number = Column("phone_number", String(13), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    picture = Column(String)    
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=True, index=True)
    created_on = Column(DateTime, default=datetime.now)

    department = relationship("Department", back_populates="users")
    role = relationship("Role", back_populates="users")
    user_cameras = relationship("UserCamera", back_populates="user", cascade = "all, delete-orphan")
    
Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone_number: str = Field(min_length=13, max_length=13)
    picture: str = Field(max_length=100)
    department_id: int | None = None
    role_id: int | None = None
    password: str = Field(min_length=8, max_length=50)

class UserOut(BaseModel):
    user_id: int
    name: str
    username: str
    email: EmailStr
    phone_number: str
    picture: str
    department_id: int | None = None
    role_id: int | None = None

    class Config:
        #orm_mode = True
        from_attributes = True

class UserUpdate(BaseModel):
    name: str = Field(default = None, min_length=2, max_length=100)
    username: str = Field(default = None, min_length=2, max_length=100)
    email: EmailStr = Field(default = None)
    phone_number: str = Field(default = None, min_length=13, max_length=13)
    picture: str = Field(default = None, max_length=100)
    department_id: int | None = None
    role_id: int | None = None
    password: str = Field(default = None, min_length=8, max_length=50)
