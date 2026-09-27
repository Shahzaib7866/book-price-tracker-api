from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from src.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    rating = Column(String, nullable=False) 
    category = Column(String, nullable=False, index=True)
    availability = Column(String, nullable=False)
    book_url = Column(String, unique=True, nullable=False)   
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())


