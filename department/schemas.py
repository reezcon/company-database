from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from engine.engine import get_connection, Base

engine = get_connection()

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(50), nullable=False, index=True)
    description = Column(String(255), nullable=True)

    users = relationship("User", back_populates = "department")

Base.metadata.create_all(bind=engine)

class DepartmentCreate(BaseModel):
    department_name: str = Field(min_length=2, max_length=50)
    description: str = Field(default=None, max_length=255)

class DepartmentOut(BaseModel):
    department_id: int
    department_name: str
    description: str

class DepartmentUpdate(BaseModel):
    department_name: str = Field(default=None, min_length=2, max_length=50)
    description: str = Field(default = None, max_length= 255)