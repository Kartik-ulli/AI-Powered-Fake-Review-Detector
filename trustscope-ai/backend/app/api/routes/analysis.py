from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ...models.analysis import ProductAnalysis, ReviewAnalysis
from ...models.review import Review
from ...models.product import Product

router = APIRouter()

@router.get("/{analysis_id}/status")
async def get_analysis_status(analysis_id: str, db: Session = Depends(get_db)):
    analysis = db.query(ProductAnalysis).filter(ProductAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {
        "id": analysis.id,
        "product_id": analysis.product_id,
        "status": analysis.status,
        "error_message": analysis.error_message,
        "total_retrieved": analysis.total_retrieved,
        "total_analysed": analysis.total_analysed,
    }

@router.get("/{analysis_id}/results")
async def get_analysis_results(analysis_id: str, db: Session = Depends(get_db)):
    analysis = db.query(ProductAnalysis).filter(ProductAnalysis.id == analysis_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    if analysis.status != "done":
        raise HTTPException(status_code=202, detail=f"Analysis {analysis.status}")
    
    product = db.query(Product).filter(Product.id == analysis.product_id).first()
    
    return {
        "analysis_id": analysis.id,
        "product": {
            "id": product.id,
            "name": product.product_name,
            "image": product.product_image,
            "platform": product.platform,
            "url": product.product_url,
            "average_rating": product.average_rating,
            "total_reviews_count": product.total_reviews_count,
            "is_demo": product.is_demo,
        },
        "summary": {
            "total_retrieved": analysis.total_retrieved,
            "total_analysed": analysis.total_analysed,
            "genuine_count": analysis.genuine_count,
            "suspicious_count": analysis.suspicious_count,
            "uncertain_count": analysis.uncertain_count,
            "genuine_pct": round(analysis.genuine_pct, 1),
            "suspicious_pct": round(analysis.suspicious_pct, 1),
            "uncertain_pct": round(analysis.uncertain_pct, 1),
            "trust_score": round(analysis.trust_score, 1),
            "high_risk_count": analysis.high_risk_count,
            "medium_risk_count": analysis.medium_risk_count,
            "low_risk_count": analysis.low_risk_count,
            "duplicate_count": analysis.duplicate_count,
            "adjusted_rating": analysis.adjusted_rating,
            "rating_distribution": analysis.rating_distribution or {},
            "ml_model_info": analysis.ml_model_info or {},
        },
        "timestamp": analysis.analysis_timestamp.isoformat() if analysis.analysis_timestamp else None,
    }
