from sqlalchemy import Column, String, Float, DateTime, Text, Boolean, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from ..database import Base

class ReviewAnalysis(Base):
    __tablename__ = "review_analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    review_id = Column(String, ForeignKey("reviews.id"), nullable=False)
    risk_score = Column(Float, default=0.0)  # 0-100
    classification = Column(String(50))  # genuine, suspicious, uncertain
    detection_reasons = Column(JSON, default=list)
    similarity_score = Column(Float, default=0.0)
    duplicate_group_id = Column(String)
    ml_prediction = Column(String(50))
    ml_confidence = Column(Float, default=0.0)
    sentiment_score = Column(Float)
    sentiment_label = Column(String(20))
    suspicious_phrases = Column(JSON, default=list)
    
    review = relationship("Review", back_populates="analysis_result")

    def __init__(self, **kwargs):
        if "id" not in kwargs or not kwargs["id"]:
            kwargs["id"] = str(uuid.uuid4())
        super().__init__(**kwargs)

class ProductAnalysis(Base):
    __tablename__ = "product_analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    total_retrieved = Column(Integer, default=0)
    total_analysed = Column(Integer, default=0)
    genuine_count = Column(Integer, default=0)
    suspicious_count = Column(Integer, default=0)
    uncertain_count = Column(Integer, default=0)
    genuine_pct = Column(Float, default=0.0)
    suspicious_pct = Column(Float, default=0.0)
    uncertain_pct = Column(Float, default=0.0)
    trust_score = Column(Float, default=0.0)
    high_risk_count = Column(Integer, default=0)
    medium_risk_count = Column(Integer, default=0)
    low_risk_count = Column(Integer, default=0)
    duplicate_count = Column(Integer, default=0)
    adjusted_rating = Column(Float)
    status = Column(String(50), default="pending")  # pending, running, done, failed
    error_message = Column(Text)
    analysis_timestamp = Column(DateTime, default=datetime.utcnow)
    rating_distribution = Column(JSON, default=dict)
    ml_model_info = Column(JSON, default=dict)
    
    product = relationship("Product", back_populates="analyses")

    def __init__(self, **kwargs):
        if "id" not in kwargs or not kwargs["id"]:
            kwargs["id"] = str(uuid.uuid4())
        super().__init__(**kwargs)
