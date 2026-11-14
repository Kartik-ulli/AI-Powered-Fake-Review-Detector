from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from ...database import get_db
from ...services.url_parser import URLParser
from ...models.product import Product
from ...models.analysis import ProductAnalysis
import logging

import uuid

router = APIRouter()
logger = logging.getLogger(__name__)

class AnalyseRequest(BaseModel):
    url: str
    demo_mode: Optional[bool] = None
    force_refresh: Optional[bool] = False

@router.post("/analyse")
async def analyse_product(request: AnalyseRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Start product analysis from URL"""
    from ...services.analysis_orchestrator import AnalysisOrchestrator
    
    # Validate URL
    url_info = URLParser.parse(request.url)
    if not url_info:
        raise HTTPException(status_code=400, detail="Invalid or unsupported product URL. Please provide an Amazon or Flipkart product URL, or use a demo URL.")
    
    # Check existing product only if force_refresh is False
    existing = db.query(Product).filter(Product.product_url == request.url).first()
    if existing and not request.force_refresh:
        existing_analysis = db.query(ProductAnalysis).filter(
            ProductAnalysis.product_id == existing.id,
            ProductAnalysis.status == "done"
        ).order_by(ProductAnalysis.analysis_timestamp.desc()).first()
        if existing_analysis:
            return {"product_id": existing.id, "analysis_id": existing_analysis.id, "cached": True}
    
    if existing:
        product = existing
    else:
        # Create product record with explicit ID
        product_id = str(uuid.uuid4())
        product = Product(
            id=product_id,
            platform=url_info["platform"],
            product_url=request.url,
            asin=url_info.get("product_id"),
            is_demo=url_info.get("is_demo", False),
        )
        db.add(product)
        db.flush()
    
    # Create analysis record (pending) with explicit ID
    analysis_id = str(uuid.uuid4())
    analysis = ProductAnalysis(id=analysis_id, product_id=product.id, status="pending")
    db.add(analysis)
    db.commit()
    db.refresh(product)
    db.refresh(analysis)
    
    # Run analysis in background
    background_tasks.add_task(
        AnalysisOrchestrator.run_full_analysis,
        product.id,
        analysis.id,
        request.url,
        url_info
    )
    
    return {"product_id": product.id, "analysis_id": analysis.id, "cached": False}

@router.get("/{product_id}")
async def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "id": product.id,
        "platform": product.platform,
        "product_name": product.product_name,
        "product_image": product.product_image,
        "average_rating": product.average_rating,
        "total_reviews_count": product.total_reviews_count,
        "product_url": product.product_url,
        "is_demo": product.is_demo,
    }
