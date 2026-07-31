from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Person(Base):
    """An actor or director ingested from TMDB, identified by TMDB's own person ID."""
    __tablename__ = "person"
    
    person_id = Column(Integer, primary_key=True, autoincrement=False)
    full_name = Column(String, nullable=False)
    
    credits = relationship("Credit", back_populates="person", cascade="all, delete-orphan")