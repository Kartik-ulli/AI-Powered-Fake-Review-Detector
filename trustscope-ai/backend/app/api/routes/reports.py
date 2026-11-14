from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from ...database import get_db
from ...models.analysis import ProductAnalysis, ReviewAnalysis
from ...models.review import Review
from ...models.product import Product
from ...services.report_generator import ReportGenerator

router = APIRouter()

@router.get("/{analysis_id}/pdf")
async def download_pdf_report(analysis_id: str, db: Session = Depends(get_db)):
    analysis = db.query(ProductAnalysis).filter(ProductAnalysis.id == analysis_id).first()
    if not analysis or analysis.status != "done":
        raise HTTPException(status_code=404, detail="Analysis not found or not complete")
    
    product = db.query(Product).filter(Product.id == analysis.product_id).first()
    
    # Get top suspicious reviews
    suspicious_reviews = db.query(Review, ReviewAnalysis).join(
        ReviewAnalysis, Review.id == ReviewAnalysis.review_id
    ).filter(
        Review.product_id == product.id,
        ReviewAnalysis.classification == "suspicious"
    ).order_by(ReviewAnalysis.risk_score.desc()).limit(10).all()
    
    pdf_bytes = ReportGenerator.generate(product, analysis, suspicious_reviews)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="trustscope-report-{analysis_id[:8]}.pdf"'}
    )
