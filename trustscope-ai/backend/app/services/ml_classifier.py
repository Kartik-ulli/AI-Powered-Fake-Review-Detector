import pickle
import logging
from typing import List, Dict
from pathlib import Path

logger = logging.getLogger(__name__)
MODEL_PATH = Path(__file__).parent.parent / "ml" / "models" / "fake_review_classifier.pkl"
METRICS_PATH = Path(__file__).parent.parent / "ml" / "models" / "model_metrics.pkl"

class MLClassifier:
    _model = None
    _metrics = None
    
    def __init__(self):
        self._load_model()
    
    def _load_model(self):
        if MLClassifier._model is not None:
            return
        try:
            if MODEL_PATH.exists():
                with open(MODEL_PATH, 'rb') as f:
                    MLClassifier._model = pickle.load(f)
                logger.info("ML model loaded successfully")
            else:
                logger.warning(f"Model not found at {MODEL_PATH}. Train with: python -m app.ml.trainer")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
        
        try:
            if METRICS_PATH.exists():
                with open(METRICS_PATH, 'rb') as f:
                    MLClassifier._metrics = pickle.load(f)
        except Exception:
            pass
    
    def predict_single(self, text: str) -> Dict:
        if not text or not text.strip():
            return {"prediction": "genuine", "confidence": 0.5}
        
        if MLClassifier._model is None:
            # Fallback: use simple heuristics
            return self._heuristic_predict(text)
        
        try:
            proba = MLClassifier._model.predict_proba([text])[0]
            pred_idx = proba.argmax()
            prediction = "fake" if pred_idx == 1 else "genuine"
            confidence = float(proba[pred_idx])
            return {"prediction": prediction, "confidence": confidence}
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return self._heuristic_predict(text)
    
    def predict_batch(self, texts: List[str]) -> List[Dict]:
        if MLClassifier._model is None:
            return [self._heuristic_predict(t) for t in texts]
        
        try:
            probas = MLClassifier._model.predict_proba(texts)
            results = []
            for proba in probas:
                pred_idx = proba.argmax()
                prediction = "fake" if pred_idx == 1 else "genuine"
                confidence = float(proba[pred_idx])
                results.append({"prediction": prediction, "confidence": confidence})
            return results
        except Exception:
            return [self._heuristic_predict(t) for t in texts]
    
    def _heuristic_predict(self, text: str) -> Dict:
        """Fallback heuristic when model is unavailable."""
        text_lower = text.lower()
        signals = 0
        for phrase in ["best ever", "must buy", "highly recommend", "amazing", "love it", "five stars", "buy now"]:
            if phrase in text_lower:
                signals += 1
        if text.count('!') >= 3:
            signals += 1
        if len(text.split()) < 10:
            signals += 1
        
        if signals >= 3:
            return {"prediction": "fake", "confidence": min(0.95, 0.6 + (signals * 0.05))}
        return {"prediction": "genuine", "confidence": 0.6}
    
    def get_model_info(self) -> Dict:
        if MLClassifier._metrics:
            return MLClassifier._metrics
        return {
            "note": "Model not trained yet. Run: python -m app.ml.trainer",
            "best_model_name": "Heuristic Fallback",
        }
