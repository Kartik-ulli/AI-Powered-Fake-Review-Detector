import logging
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models.product import Product
from ..models.review import Review
from ..models.analysis import ProductAnalysis, ReviewAnalysis
from .review_fetcher import ReviewFetcher
from .nlp_pipeline import NLPPipeline
from .ml_classifier import MLClassifier
from .duplicate_detector import DuplicateDetector
from .risk_scorer import RiskScorer
from .trust_calculator import TrustCalculator

logger = logging.getLogger(__name__)

class AnalysisOrchestrator:
    @staticmethod
    async def run_full_analysis(product_id: str, analysis_id: str, url: str, url_info: dict):
        db = SessionLocal()
        try:
            analysis = db.query(ProductAnalysis).filter(ProductAnalysis.id == analysis_id).first()
            if not analysis:
                logger.error(f"Analysis {analysis_id} not found")
                return
            analysis.status = "running"
            db.commit()
            
            # 1. Fetch reviews
            logger.info(f"Fetching reviews for product {product_id}")
            data = await ReviewFetcher.fetch(url_info["platform"], url_info.get("product_id"), url_info)
            
            product_info = data["product_info"]
            raw_reviews = data["reviews"]
            
            # 2. Update product info
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                product.product_name = product_info.get("product_name", "Unknown Product")
                product.product_image = product_info.get("product_image", "")
                product.average_rating = product_info.get("average_rating")
                product.total_reviews_count = product_info.get("total_reviews_count", str(len(raw_reviews)))
                db.commit()
            
            # 3. Store reviews in DB
            review_objects = []
            for rv in raw_reviews:
                text = rv.get("review_text", "").strip()
                if not text:
                    continue
                r = Review(
                    product_id=product_id,
                    review_text=text,
                    star_rating=rv.get("star_rating"),
                    reviewer_id=rv.get("reviewer_id"),
                    reviewer_name=rv.get("reviewer_name", "Anonymous"),
                    review_date=rv.get("review_date", ""),
                    verified_purchase=rv.get("verified_purchase", False),
                    helpful_votes=rv.get("helpful_votes", 0),
                    review_title=rv.get("review_title", ""),
                )
                db.add(r)
                review_objects.append(r)
            db.commit()
            
            analysis.total_retrieved = len(raw_reviews)
            analysis.total_analysed = len(review_objects)
            db.commit()
            
            # 4. NLP Analysis
            logger.info(f"Running NLP analysis on {len(review_objects)} reviews")
            nlp = NLPPipeline()
            nlp_results = nlp.analyse_batch([r.review_text for r in review_objects])
            
            # 5. Duplicate Detection
            logger.info("Detecting duplicates with TF-IDF cosine similarity...")
            dup_groups = DuplicateDetector.detect([r.review_text for r in review_objects])
            
            # 6. ML Classification
            logger.info("Running ML classification predictions...")
            ml_clf = MLClassifier()
            ml_results = ml_clf.predict_batch([r.review_text for r in review_objects])
            
            # 7. Risk Scoring & Save Results
            risk_scorer = RiskScorer()
            review_analysis_objects = []
            
            for i, review in enumerate(review_objects):
                nlp_r = nlp_results[i]
                ml_r = ml_results[i]
                dup_r = dup_groups.get(i, {})
                
                risk_score, reasons = risk_scorer.score(nlp_r, ml_r, dup_r, review.star_rating)
                classification = RiskScorer.classify(risk_score)
                
                ra = ReviewAnalysis(
                    review_id=review.id,
                    risk_score=risk_score,
                    classification=classification,
                    detection_reasons=reasons,
                    similarity_score=dup_r.get("max_similarity", 0.0),
                    duplicate_group_id=dup_r.get("group_id"),
                    ml_prediction=ml_r.get("prediction", "genuine"),
                    ml_confidence=ml_r.get("confidence", 0.0),
                    sentiment_score=nlp_r.get("sentiment_score"),
                    sentiment_label=nlp_r.get("sentiment_label"),
                    suspicious_phrases=nlp_r.get("suspicious_phrases", []),
                )
                db.add(ra)
                review_analysis_objects.append(ra)
            
            db.commit()
            
            # 8. Calculate Trust Score & Aggregate Stats
            trust_data = TrustCalculator.calculate(
                review_analysis_objects,
                product.average_rating if product else None,
                analysis.total_analysed
            )
            
            # Rating distribution
            rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for r in review_objects:
                if r.star_rating:
                    star = int(round(r.star_rating))
                    if 1 <= star <= 5:
                        rating_dist[star] = rating_dist.get(star, 0) + 1
            
            # 9. Update ProductAnalysis
            analysis.genuine_count = trust_data["genuine_count"]
            analysis.suspicious_count = trust_data["suspicious_count"]
            analysis.uncertain_count = trust_data["uncertain_count"]
            analysis.genuine_pct = trust_data["genuine_pct"]
            analysis.suspicious_pct = trust_data["suspicious_pct"]
            analysis.uncertain_pct = trust_data["uncertain_pct"]
            analysis.trust_score = trust_data["trust_score"]
            analysis.high_risk_count = trust_data["high_risk_count"]
            analysis.medium_risk_count = trust_data["medium_risk_count"]
            analysis.low_risk_count = trust_data["low_risk_count"]
            analysis.duplicate_count = trust_data["duplicate_count"]
            analysis.adjusted_rating = trust_data["adjusted_rating"]
            analysis.rating_distribution = rating_dist
            analysis.ml_model_info = ml_clf.get_model_info()
            analysis.status = "done"
            db.commit()
            
            logger.info(f"Analysis complete. Trust score: {trust_data['trust_score']:.1f}")
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}", exc_info=True)
            if db:
                analysis = db.query(ProductAnalysis).filter(ProductAnalysis.id == analysis_id).first()
                if analysis:
                    analysis.status = "failed"
                    analysis.error_message = str(e)
                    db.commit()
        finally:
            db.close()
