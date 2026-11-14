from typing import Dict, Tuple, List

class RiskScorer:
    @staticmethod
    def score(nlp_result: Dict, ml_result: Dict, dup_result: Dict, star_rating: float = None) -> Tuple[float, List[str]]:
        """Calculate 0-100 risk score and list of detection reasons."""
        score = 0.0
        reasons = []
        
        # === NLP Signals (max 40 points) ===
        nlp_signals = nlp_result.get("nlp_suspicion_signals", 0)
        
        if nlp_result.get("is_too_short"):
            score += 8
            reasons.append("Unusually short review (fewer than 5 words)")
        
        if nlp_result.get("suspicious_phrase_count", 0) >= 2:
            score += min(nlp_result["suspicious_phrase_count"] * 5, 15)
            reasons.append(f"Contains {nlp_result['suspicious_phrase_count']} promotional/generic phrases")
        elif nlp_result.get("suspicious_phrase_count", 0) == 1:
            score += 5
            reasons.append(f"Contains generic marketing phrase: '{nlp_result['suspicious_phrases'][0]}'")
        
        if nlp_result.get("excessive_exclamation"):
            score += 8
            reasons.append(f"Excessive exclamation marks ({nlp_result['exclamation_count']})")
        
        if nlp_result.get("has_excessive_caps"):
            score += 5
            reasons.append("Unusual use of capitalized words")
        
        if nlp_result.get("has_promotional"):
            score += 10
            reasons.append("Contains promotional language patterns")
        
        if nlp_result.get("has_repetition"):
            score += 7
            reasons.append("Repetitive word usage detected")
        
        # Rating-sentiment mismatch
        if star_rating is not None:
            if star_rating <= 2 and nlp_result.get("sentiment_positive"):
                score += 12
                reasons.append("Rating-sentiment mismatch: low rating but very positive text")
            elif star_rating >= 4 and nlp_result.get("sentiment_negative"):
                score += 12
                reasons.append("Rating-sentiment mismatch: high rating but negative text")
        
        # === Duplicate Detection (max 35 points) ===
        max_sim = dup_result.get("max_similarity", 0.0)
        if max_sim >= 0.98:
            score += 35
            reasons.append("Exact duplicate of another review")
        elif max_sim >= 0.85:
            score += 25
            reasons.append(f"Highly similar to other reviews ({max_sim:.0%} similarity)")
        elif max_sim >= 0.75:
            score += 15
            reasons.append(f"Moderately similar to other reviews ({max_sim:.0%} similarity)")
        
        # === ML Prediction (max 25 points) ===
        ml_pred = ml_result.get("prediction", "genuine")
        ml_conf = ml_result.get("confidence", 0.5)
        if ml_pred == "fake":
            score += max(10, min(25, int(ml_conf * 25)))
            reasons.append(f"ML model classified as suspicious (confidence: {ml_conf:.0%})")
        
        # Cap at 100
        score = min(100.0, score)
        return round(score, 1), reasons
    
    @staticmethod
    def classify(risk_score: float) -> str:
        if risk_score <= 30:
            return "genuine"
        elif risk_score <= 60:
            return "uncertain"
        else:
            return "suspicious"
