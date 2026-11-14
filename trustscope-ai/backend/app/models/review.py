from sqlalchemy import Column, String, Float, DateTime, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    review_text = Column(Text, nullable=False)
    star_rating = Column(Float)
    reviewer_id = Column(String(255))
    reviewer_name = Column(String(255))
    review_date = Column(String(100))
    verified_purchase = Column(Boolean, default=False)
    helpful_votes = Column(Integer, default=0)
    review_title = Column(Text)
    
    product = relationship("Product", back_populates="reviews")
    analysis_result = relationship("ReviewAnalysis", back_populates="review", uselist=False, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        if "id" not in kwargs or not kwargs["id"]:
            kwargs["id"] = str(uuid.uuid4())
        super().__init__(**kwargs)
