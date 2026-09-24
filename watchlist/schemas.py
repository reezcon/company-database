from datetime import datetime 

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from engine.engine import Base 

class Watchlist(Base):
    __tablename__ = 'watchlist'

    watchlist_id = Column(Integer, primary_key = True, index = True)
    watchlist_name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    users = relationship("User", back_populates="watchlist")

class WatchlistCreate(BaseModel):
    watchlist_name: str = Field(min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=255)

class WatchlistOut(BaseModel):
    watchlist_id: int
    watchlist_name: str
    description: str | None = None

    class Config: 
        from_attributes = True

class WatchlistUpdate(BaseModel):
    watchlist_name: str = Field(min_length=2, max_length=255)
    description: str = Field(default=None, max_length = 255)