from .database import Base
from sqlalchemy import Column, String, Integer

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)
    genre = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)

