"""Modelo ORM para la tabla 'person'."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Person(Base):
    __tablename__ = "person"
    
    person_id = Column(Integer, primary_key=True, autoincrement=False)
    full_name = Column(String, nullable=False)
    
    credits = relationship("Credit", back_populates="person", cascade="all, delete-orphan")