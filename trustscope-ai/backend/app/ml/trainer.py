"""
TrustScope AI — ML Model Training on the Ott et al. Deceptive Opinion Spam Benchmark Dataset (op_spam_v1.4).

Dataset:
- 800 Deceptive Reviews (Crowdsourced deceptive opinion spam via Amazon Mechanical Turk)
- 800 Truthful Reviews (Mining verified genuine reviews from TripAdvisor & Web)
Total: 1,600 real-world benchmark instances across positive and negative polarities.

Run: python -m app.ml.trainer
"""

import os
import pickle
import logging
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
MODEL_DIR = BASE_DIR / "ml" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "fake_review_classifier.pkl"
METRICS_PATH = MODEL_DIR / "model_metrics.pkl"
DATASET_DIR = BASE_DIR / "ml" / "datasets" / "op_spam" / "op_spam_v1.4"


def load_op_spam_dataset():
    """Load reviews and labels from the Ott et al. op_spam_v1.4 dataset."""
    texts = []
    labels = []  # 1 = deceptive/fake, 0 = truthful/genuine
    metadata = []

    if not DATASET_DIR.exists():
        logger.warning(f"Dataset path {DATASET_DIR} does not exist. Looking in parent directories...")
        alt_path = Path("app/ml/datasets/op_spam/op_spam_v1.4")
        if alt_path.exists():
            search_dir = alt_path
        else:
            raise FileNotFoundError(f"Cannot find op_spam_v1.4 dataset at {DATASET_DIR}")
    else:
        search_dir = DATASET_DIR

    deceptive_files = list(search_dir.glob("**/deceptive*/**/*.txt"))
    truthful_files = list(search_dir.glob("**/truthful*/**/*.txt"))

    logger.info(f"Discovered {len(deceptive_files)} deceptive review files and {len(truthful_files)} truthful review files.")

    for p in deceptive_files:
        try:
            content = p.read_text(encoding="utf-8", errors="ignore").strip()
            if content:
                texts.append(content)
                labels.append(1)
                polarity = "negative" if "negative" in str(p) else "positive"
                metadata.append({"polarity": polarity, "type": "deceptive"})
        except Exception as e:
            logger.warning(f"Error reading {p}: {e}")

    for p in truthful_files:
        try:
            content = p.read_text(encoding="utf-8", errors="ignore").strip()
            if content:
                texts.append(content)
                labels.append(0)
                polarity = "negative" if "negative" in str(p) else "positive"
                metadata.append({"polarity": polarity, "type": "truthful"})
        except Exception as e:
            logger.warning(f"Error reading {p}: {e}")

    return texts, labels, metadata


def train_and_evaluate():
    """Train multiple models on op_spam_v1.4, compare performance, and save the best model."""
    logger.info("Loading Ott Deceptive Opinion Spam benchmark dataset...")
    texts, labels, metadata = load_op_spam_dataset()
    logger.info(f"Loaded {len(texts)} total labelled reviews ({labels.count(1)} deceptive, {labels.count(0)} truthful).")

    # 80/20 train/test split stratified by label
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.20, random_state=42, stratify=labels
    )

    models = {
        "Logistic Regression (TF-IDF)": Pipeline([
            ("tfidf", TfidfVectorizer(
                max_features=12000,
                ngram_range=(1, 2),
                sublinear_tf=True,
                strip_accents="unicode",
                min_df=2
            )),
            ("clf", LogisticRegression(max_iter=1000, C=2.0, random_state=42)),
        ]),
        "Linear SVM (Calibrated)": Pipeline([
            ("tfidf", TfidfVectorizer(
                max_features=12000,
                ngram_range=(1, 2),
                sublinear_tf=True,
                strip_accents="unicode",
                min_df=2
            )),
            ("clf", CalibratedClassifierCV(LinearSVC(C=1.0, random_state=42), cv=3)),
        ]),
        "Naive Bayes (Multinomial)": Pipeline([
            ("tfidf", TfidfVectorizer(
                max_features=12000,
                ngram_range=(1, 2),
                strip_accents="unicode",
                min_df=2
            )),
            ("clf", MultinomialNB(alpha=0.1)),
        ]),
        "Random Forest Classifier": Pipeline([
            ("tfidf", TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                min_df=2
            )),
            ("clf", RandomForestClassifier(n_estimators=150, max_depth=30, random_state=42, n_jobs=-1)),
        ]),
    }

    best_model = None
    best_f1 = 0.0
    best_name = ""
    all_metrics = {}

    for name, pipeline in models.items():
        logger.info(f"Training {name}...")
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        all_metrics[name] = {
            "accuracy": round(float(acc), 4),
            "precision": round(float(prec), 4),
            "recall": round(float(rec), 4),
            "f1_score": round(float(f1), 4),
            "confusion_matrix": cm,
        }

        logger.info(f"  -> {name} | Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_model = pipeline
            best_name = name

    logger.info(f"\n=======================================================")
    logger.info(f"Best Performing Model: {best_name} (F1 = {best_f1:.4f})")
    logger.info(f"=======================================================\n")

    # Save best pipeline
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(best_model, f)

    metrics_data = {
        "best_model_name": best_name,
        "best_f1": round(float(best_f1), 4),
        "all_metrics": all_metrics,
        "training_samples": len(X_train),
        "test_samples": len(X_test),
        "dataset_name": "Ott et al. Deceptive Opinion Spam (op_spam_v1.4)",
        "total_instances": len(texts),
        "deceptive_count": labels.count(1),
        "truthful_count": labels.count(0),
        "note": "Trained on the gold-standard Ott et al. Deceptive Opinion Spam Corpus (1,600 verified reviews). Predictions indicate deceptive probability."
    }

    with open(METRICS_PATH, "wb") as f:
        pickle.dump(metrics_data, f)

    logger.info(f"Model saved to {MODEL_PATH}")
    logger.info(f"Metrics saved to {METRICS_PATH}")
    return metrics_data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    result = train_and_evaluate()
    print("\n--- Model Training Summary ---")
    for name, m in result["all_metrics"].items():
        print(f"\nModel: {name}")
        print(f"  Accuracy:  {m['accuracy']*100:.2f}%")
        print(f"  Precision: {m['precision']*100:.2f}%")
        print(f"  Recall:    {m['recall']*100:.2f}%")
        print(f"  F1-Score:  {m['f1_score']*100:.2f}%")
        print(f"  Confusion Matrix: {m['confusion_matrix']}")
    print(f"\nBest Model Selected for Production: {result['best_model_name']}")
