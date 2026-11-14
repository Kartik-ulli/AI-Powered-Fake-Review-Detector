from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from ...database import get_db
from ...models.review import Review
from ...models.analysis import ReviewAnalysis, ProductAnalysis
from ...models.product import Product

router = APIRouter()

@router.get("/product/{product_id}")
async def get_product_reviews(
    product_id: str,
    classification: Optional[str] = Query(None, description="Filter: genuine, suspicious, uncertain"),
    risk_level: Optional[str] = Query(None, description="Filter: high, medium, low"),
    search: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("risk_score_desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Review, ReviewAnalysis).join(
        ReviewAnalysis, Review.id == ReviewAnalysis.review_id
    ).filter(Review.product_id == product_id)
    
    if classification:
        query = query.filter(ReviewAnalysis.classification == classification)
    
    if risk_level == "high":
        query = query.filter(ReviewAnalysis.risk_score >= 61)
    elif risk_level == "medium":
        query = query.filter(ReviewAnalysis.risk_score.between(31, 60))
    elif risk_level == "low":
        query = query.filter(ReviewAnalysis.risk_score <= 30)
    
    if search:
        query = query.filter(Review.review_text.ilike(f"%{search}%"))
    
    # Sorting
    if sort_by == "risk_score_desc":
        query = query.order_by(ReviewAnalysis.risk_score.desc())
    elif sort_by == "risk_score_asc":
        query = query.order_by(ReviewAnalysis.risk_score.asc())
    elif sort_by == "rating_desc":
        query = query.order_by(Review.star_rating.desc())
    elif sort_by == "rating_asc":
        query = query.order_by(Review.star_rating.asc())
    
    total = query.count()
    results = query.offset((page - 1) * page_size).limit(page_size).all()
    
    reviews = []
    for review, ra in results:
        reviews.append({
            "id": review.id,
            "text": review.review_text,
            "title": review.review_title,
            "rating": review.star_rating,
            "reviewer_name": review.reviewer_name,
            "date": review.review_date,
            "verified_purchase": review.verified_purchase,
            "helpful_votes": review.helpful_votes,
            "risk_score": round(ra.risk_score, 1),
            "classification": ra.classification,
            "detection_reasons": ra.detection_reasons or [],
            "suspicious_phrases": ra.suspicious_phrases or [],
            "sentiment_score": ra.sentiment_score,
            "sentiment_label": ra.sentiment_label,
            "similarity_score": round(ra.similarity_score or 0, 3),
            "duplicate_group_id": ra.duplicate_group_id,
            "ml_prediction": ra.ml_prediction,
            "ml_confidence": round(ra.ml_confidence or 0, 3),
        })
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "reviews": reviews,
    }

@router.get("/{review_id}/duplicates")
async def get_review_duplicates(review_id: str, db: Session = Depends(get_db)):
    ra = db.query(ReviewAnalysis).filter(ReviewAnalysis.review_id == review_id).first()
    if not ra or not ra.duplicate_group_id:
        return {"duplicates": []}
    
    group_members = db.query(Review, ReviewAnalysis).join(
        ReviewAnalysis, Review.id == ReviewAnalysis.review_id
    ).filter(
        ReviewAnalysis.duplicate_group_id == ra.duplicate_group_id,
        Review.id != review_id
    ).all()
    
    return {
        "duplicates": [
            {
                "id": r.id,
                "text": r.review_text[:200] + "..." if len(r.review_text) > 200 else r.review_text,
                "similarity_score": round(ra2.similarity_score or 0, 3),
                "classification": ra2.classification,
            }
            for r, ra2 in group_members
        ]
    }
