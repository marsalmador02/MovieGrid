"""Modelo ORM para la tabla 'credit'."""

from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Credit(Base):
    __tablename__ = "credit"
    
    credit_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movie.movie_id", ondelete="CASCADE"), nullable=False, index=True)
    person_id = Column(Integer, ForeignKey("person.person_id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    character_name = Column(String, nullable=True)
    
    __table_args__ = (
        CheckConstraint("role IN ('ACTOR', 'DIRECTOR')", name="valid_roles"),
    )
    
    movie = relationship("Movie", back_populates="credits")
    person = relationship("Person", back_populates="credits")