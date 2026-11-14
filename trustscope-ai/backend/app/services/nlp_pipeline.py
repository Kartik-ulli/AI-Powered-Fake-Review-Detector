import re
import logging
from typing import List, Dict, Optional
from collections import Counter

logger = logging.getLogger(__name__)

SUSPICIOUS_PHRASES = [
    "best product ever", "must buy", "highly recommend", "amazing quality",
    "five stars", "love this product", "perfect product", "excellent product",
    "buy now", "don't miss", "great value", "worth every penny",
    "changed my life", "absolutely love", "can't live without",
    "life changing", "game changer", "must have", "exceeded expectations",
    "blown away", "so happy", "very satisfied"
]

PROMOTIONAL_PATTERNS = [
    r'buy now', r'order now', r'click here', r'check it out',
    r'visit.*website', r'follow.*link', r'discount code',
    r'use code', r'promo', r'sale.*%', r'limited.*time',
]

class NLPPipeline:
    def __init__(self):
        self._init_nltk()
        self._init_vader()
        self._suspicious_phrases = SUSPICIOUS_PHRASES
        self._promo_patterns = [re.compile(p, re.IGNORECASE) for p in PROMOTIONAL_PATTERNS]
    
    def _init_nltk(self):
        try:
            import nltk
            self._use_nltk = True
        except ImportError:
            self._use_nltk = False
    
    def _init_vader(self):
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self._vader = SentimentIntensityAnalyzer()
            self._use_vader = True
        except Exception:
            self._use_vader = False
    
    def _tokenize(self, text: str) -> List[str]:
        try:
            if self._use_nltk:
                import nltk
                return nltk.word_tokenize(text.lower())
        except Exception:
            pass
        return re.findall(r'\b\w+\b', text.lower())
    
    def _get_sentiment(self, text: str) -> Dict:
        if self._use_vader:
            scores = self._vader.polarity_scores(text)
            compound = scores['compound']
            if compound >= 0.05:
                label = "positive"
            elif compound <= -0.05:
                label = "negative"
            else:
                label = "neutral"
            return {"sentiment_score": round(compound, 4), "sentiment_label": label}
        return {"sentiment_score": 0.0, "sentiment_label": "neutral"}
    
    def analyse_single(self, text: str) -> Dict:
        if not text or not text.strip():
            return self._empty_result()
        
        result = {}
        
        # Sentiment
        result.update(self._get_sentiment(text))
        
        # Length analysis
        word_count = len(text.split())
        result["word_count"] = word_count
        result["is_too_short"] = word_count < 5
        result["is_too_long"] = word_count > 500
        result["is_unusual_length"] = word_count < 3 or word_count > 600
        
        # Suspicious phrases
        text_lower = text.lower()
        found_suspicious = []
        for phrase in self._suspicious_phrases:
            if phrase in text_lower:
                found_suspicious.append(phrase)
        result["suspicious_phrases"] = found_suspicious
        result["suspicious_phrase_count"] = len(found_suspicious)
        
        # Promotional language
        promo_matches = []
        for pat in self._promo_patterns:
            m = pat.search(text)
            if m:
                promo_matches.append(m.group())
        result["promotional_patterns"] = promo_matches
        result["has_promotional"] = len(promo_matches) > 0
        
        # Exclamation marks (excessive excitement)
        excl_count = text.count('!')
        result["exclamation_count"] = excl_count
        result["excessive_exclamation"] = excl_count >= 3
        
        # ALL CAPS words (shouting)
        words = text.split()
        caps_words = [w for w in words if len(w) > 2 and w.isupper()]
        result["caps_word_count"] = len(caps_words)
        result["has_excessive_caps"] = len(caps_words) >= 3
        
        # Repetition detection
        word_freq = Counter(text_lower.split())
        most_common = word_freq.most_common(5)
        repeated_words = [w for w, c in most_common if c > 3 and len(w) > 3]
        result["repeated_words"] = repeated_words
        result["has_repetition"] = len(repeated_words) > 0
        
        # Star/emoji patterns
        result["has_star_spam"] = bool(re.search(r'[★☆✓✔]{2,}', text))
        
        # Rating-sentiment mismatch signals (determined later with star_rating)
        result["sentiment_positive"] = result["sentiment_score"] > 0.5
        result["sentiment_negative"] = result["sentiment_score"] < -0.3
        
        # Overall suspicion signals
        result["nlp_suspicion_signals"] = (
            result["suspicious_phrase_count"] +
            (1 if result["excessive_exclamation"] else 0) +
            (1 if result["has_excessive_caps"] else 0) +
            (1 if result["has_promotional"] else 0) +
            (1 if result["has_repetition"] else 0) +
            (1 if result["is_too_short"] else 0)
        )
        
        return result
    
    def analyse_batch(self, texts: List[str]) -> List[Dict]:
        return [self.analyse_single(t) for t in texts]
    
    def _empty_result(self) -> Dict:
        return {
            "sentiment_score": 0.0, "sentiment_label": "neutral",
            "word_count": 0, "is_too_short": True, "is_too_long": False,
            "is_unusual_length": True, "suspicious_phrases": [],
            "suspicious_phrase_count": 0, "promotional_patterns": [],
            "has_promotional": False, "exclamation_count": 0,
            "excessive_exclamation": False, "caps_word_count": 0,
            "has_excessive_caps": False, "repeated_words": [],
            "has_repetition": False, "has_star_spam": False,
            "sentiment_positive": False, "sentiment_negative": False,
            "nlp_suspicion_signals": 2,
        }
