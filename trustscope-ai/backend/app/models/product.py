from sqlalchemy import Column, String, Float, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    platform = Column(String(50), nullable=False)  # amazon, flipkart, demo
    product_url = Column(Text, nullable=False)
    product_name = Column(Text)
    product_image = Column(Text)
    average_rating = Column(Float)
    total_reviews_count = Column(String(50))
    asin = Column(String(50))  # Amazon ASIN or Flipkart ID
    created_at = Column(DateTime, default=datetime.utcnow)
    is_demo = Column(Boolean, default=False)
    
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    analyses = relationship("ProductAnalysis", back_populates="product", cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        if "id" not in kwargs or not kwargs["id"]:
            kwargs["id"] = str(uuid.uuid4())
        super().__init__(**kwargs)
