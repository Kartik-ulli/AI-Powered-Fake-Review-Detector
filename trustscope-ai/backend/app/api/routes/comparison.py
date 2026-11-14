from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ...database import get_db
from ...services.url_parser import URLParser
from ...models.product import Product
from ...models.analysis import ProductAnalysis

router = APIRouter()

class CompareRequest(BaseModel):
    url1: str
    url2: str

@router.post("/")
async def compare_products(request: CompareRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    from ...api.routes.products import analyse_product, AnalyseRequest
    
    result1 = await analyse_product(AnalyseRequest(url=request.url1), background_tasks, db)
    result2 = await analyse_product(AnalyseRequest(url=request.url2), background_tasks, db)
    
    return {
        "product1_id": result1["product_id"],
        "analysis1_id": result1["analysis_id"],
        "product2_id": result2["product_id"],
        "analysis2_id": result2["analysis_id"],
    }

@router.get("/{analysis1_id}/{analysis2_id}")
async def get_comparison(analysis1_id: str, analysis2_id: str, db: Session = Depends(get_db)):
    def get_analysis_data(analysis_id):
        a = db.query(ProductAnalysis).filter(ProductAnalysis.id == analysis_id).first()
        if not a:
            return None
        p = db.query(Product).filter(Product.id == a.product_id).first()
        return {"analysis": a, "product": p}
    
    d1 = get_analysis_data(analysis1_id)
    d2 = get_analysis_data(analysis2_id)
    
    if not d1 or not d2:
        raise HTTPException(status_code=404, detail="One or both analyses not found")
    
    def fmt(d):
        a, p = d["analysis"], d["product"]
        return {
            "product_name": p.product_name,
            "platform": p.platform,
            "average_rating": p.average_rating,
            "status": a.status,
            "trust_score": round(a.trust_score or 0, 1),
            "genuine_pct": round(a.genuine_pct or 0, 1),
            "suspicious_pct": round(a.suspicious_pct or 0, 1),
            "uncertain_pct": round(a.uncertain_pct or 0, 1),
            "total_analysed": a.total_analysed,
            "duplicate_count": a.duplicate_count,
            "adjusted_rating": a.adjusted_rating,
        }
    
    return {"product1": fmt(d1), "product2": fmt(d2)}
