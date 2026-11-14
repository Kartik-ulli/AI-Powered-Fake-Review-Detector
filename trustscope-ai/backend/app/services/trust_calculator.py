from typing import List, Dict
from collections import Counter

class TrustCalculator:
    @staticmethod
    def calculate(review_analyses: list, avg_rating: float, total_analysed: int) -> Dict:
        if not review_analyses:
            return {
                "genuine_count": 0, "suspicious_count": 0, "uncertain_count": 0,
                "genuine_pct": 0.0, "suspicious_pct": 0.0, "uncertain_pct": 0.0,
                "trust_score": 50.0, "high_risk_count": 0, "medium_risk_count": 0,
                "low_risk_count": 0, "duplicate_count": 0, "adjusted_rating": avg_rating,
                "rating_distribution": {},
            }
        
        total = len(review_analyses)
        genuine = sum(1 for ra in review_analyses if ra.classification == "genuine")
        suspicious = sum(1 for ra in review_analyses if ra.classification == "suspicious")
        uncertain = sum(1 for ra in review_analyses if ra.classification == "uncertain")
        high_risk = sum(1 for ra in review_analyses if ra.risk_score >= 61)
        medium_risk = sum(1 for ra in review_analyses if 31 <= ra.risk_score < 61)
        low_risk = sum(1 for ra in review_analyses if ra.risk_score < 31)
        
        # Count duplicates (reviews in a group)
        seen_groups = set()
        duplicate_count = 0
        for ra in review_analyses:
            if ra.duplicate_group_id and ra.duplicate_group_id not in seen_groups:
                seen_groups.add(ra.duplicate_group_id)
            elif ra.duplicate_group_id:
                duplicate_count += 1
        
        # Exact percentages specified in requirements
        genuine_pct = (genuine / total) * 100
        suspicious_pct = (suspicious / total) * 100
        uncertain_pct = (uncertain / total) * 100
        
        # Trust score formula (0 - 100)
        # Base: start at 100, deduct for suspicious %, high risk %, duplicates
        suspicious_penalty = (suspicious / total) * 45
        high_risk_penalty = (high_risk / total) * 25
        dup_penalty = min((duplicate_count / max(total, 1)) * 20, 20)
        trust_score = max(0.0, min(100.0, 100.0 - suspicious_penalty - high_risk_penalty - dup_penalty))
        
        # Adjusted rating: weight genuine reviews more
        if avg_rating:
            # If high proportion of suspicious, lower the displayed rating
            adjustment = (suspicious / total) * 0.75
            adjusted = max(1.0, min(5.0, (avg_rating or 3.0) - adjustment))
        else:
            adjusted = None
        
        return {
            "genuine_count": genuine,
            "suspicious_count": suspicious,
            "uncertain_count": uncertain,
            "genuine_pct": genuine_pct,
            "suspicious_pct": suspicious_pct,
            "uncertain_pct": uncertain_pct,
            "trust_score": trust_score,
            "high_risk_count": high_risk,
            "medium_risk_count": medium_risk,
            "low_risk_count": low_risk,
            "duplicate_count": duplicate_count,
            "adjusted_rating": round(adjusted, 2) if adjusted else None,
            "rating_distribution": {},
        }
