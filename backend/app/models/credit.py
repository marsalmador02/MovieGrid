from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Credit(Base):
    __tablename__ = "credit"

    credit_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, ForeignKey("movie.movie_id", ondelete="CASCADE"), nullable=False)
    person_id = Column(Integer, ForeignKey("person.person_id", ondelete="CASCADE"), nullable=False)
    role = Column(String(20), nullable=False)
    character_name = Column(String, nullable=True)

    __table_args__ = (
        CheckConstraint("role IN ('ACTOR', 'DIRECTOR')", name="valid_roles"),
        UniqueConstraint("movie_id", "person_id", "role", name="unique_movie_person_role"),
        Index("ix_credit_movie_id", "movie_id"),
        Index("ix_credit_person_id", "person_id"),
        Index("idx_credit_movie_person", "movie_id", "person_id"),
        Index("idx_credit_person_role", "person_id", "role"),
    )

    movie = relationship("Movie", back_populates="credits")
    person = relationship("Person", back_populates="credits")