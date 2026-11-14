# TRUSTSCOPE AI 🔍
### *Know Which Reviews to Trust Before You Buy.*

> **College Hackathon Engineering Submission**  
> An end-to-end, AI-powered Fake Product Review Detection and Consumer Trust Intelligence Platform built from scratch.

---

## 🎯 1. Problem Statement & Proposed Solution

E-commerce marketplaces contain millions of reviews, yet a significant portion are fabricated, incentivized, copied, or bot-generated to artificially inflate product ratings. Consumers struggle to separate authentic feedback from deceptive marketing, leading to poor purchasing decisions and lost consumer trust.

**TrustScope AI** addresses this with a zero-friction paradigm:
- **Zero manual copying**: The user only pastes an Amazon or Flipkart link.
- **Autonomous collection**: The system extracts product metadata and customer reviews.
- **Multi-signal AI analysis**: Evaluates reviews using NLP stylistic markers, TF-IDF duplicate detection, and trained Machine Learning deception classifiers.
- **Explainable Trust Dashboard**: Generates calibrated product trust percentages, risk breakdowns, explainable reasons, and downloadable PDF reports.

---

## 🏗️ 2. Architectural Overview

```
                                +---------------------------+
                                |  React 18 + Tailwind CSS  |
                                |      (Vite Frontend)      |
                                +-------------+-------------+
                                              |
                                              | REST APIs (Axios)
                                              v
                                +-------------+-------------+
                                |      FastAPI Backend      |
                                +-------------+-------------+
                                              |
     +-------------------+--------------------+--------------------+--------------------+
     |                   |                    |                    |                    |
     v                   v                    v                    v                    v
+----+----+         +----+----+          +----+----+          +----+----+          +----+----+
| URL     |         | Review  |          | NLP     |          | TF-IDF  |          | ML      |
| Parser  |         | Fetcher |          | Pipeline|          | Cosine  |          | Models  |
+---------+         +---------+          +---------+          +---------+          +---------+
 (Amazon/            (Live API /          (VADER,              (Near-               (Logistic,
  Flipkart /          Demo Mode)           Stylistics,          Duplicate            Random Forest,
  Demo URLs)                               Phrases)             Clustering)          Naive Bayes)
     |                   |                    |                    |                    |
     +-------------------+--------------------+--------------------+--------------------+
                                              |
                                              v
                                +-------------+-------------+
                                |    Risk Scoring Engine    |
                                |     (0-100 Risk Score)    |
                                +-------------+-------------+
                                              |
                                              v
                                +-------------+-------------+
                                |    Trust Score Calculator |
                                |  (Genuine/Suspicious/Unc) |
                                +-------------+-------------+
                                              |
                                              v
                                +-------------+-------------+
                                |  SQLite DB + ReportLab    |
                                |     (PDF Generation)      |
                                +---------------------------+
```

---

## 🚀 3. Quick Start (How to Run)

### Method 1: 1-Click Launch (Recommended on Windows)
Simply double-click:
```bat
start_all.bat
```
This automatically launches both backend (`http://localhost:8000`) and frontend (`http://localhost:5173`).

---

### Method 2: Manual Terminal Launch

#### Backend
```bash
cd backend
# Run with Python:
python -m uvicorn app.main:app --reload --port 8000
```
API Documentation will be live at: **http://localhost:8000/docs**

#### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open **http://localhost:5173** in your browser.

*(Note: The frontend production build is also bundled directly inside `frontend/dist` and served automatically by the backend at `http://localhost:8000`)*

---

## 🧪 4. Hackathon Demonstration Mode

For judge demonstrations without external API quotas, TrustScope AI features **1-Click Pre-loaded Demo Products**:

1. **Mostly Genuine Product** (`https://www.amazon.com/dp/DEMO001`):
   - *EcoBreeze Stainless Steel Water Bottle 1L*
   - Authentic linguistic diversity, detailed experience stories, constructive criticism.
   - Result: High Trust Score (~100/100), 100% Genuine.

2. **High Suspiciousness Product** (`https://www.amazon.com/dp/DEMO002`):
   - *UltraSlim Pro X Weight Loss Supplement*
   - Copy-pasted duplicates, promotional hype words ("Buy now!!", "Life changing!!"), extreme exclamation spam, low verified purchase ratio.
   - Result: Low Trust Score, flagged duplicate review clusters.

3. **Mixed Review Profile** (`https://www.amazon.com/dp/DEMO003`):
   - *TechFlow Wireless Bluetooth Earbuds*
   - Realistic blend of authentic buyer feedback mixed with coordinated marketing reviews.

---

## 📊 5. Key Features & Acceptance Criteria Met

| # | Requirement | Status | Implementation Details |
|---|---|:---:|---|
| 1 | Single URL Input | ✅ | Supports Amazon, Flipkart, and Demo protocol URLs |
| 2 | Product Identification | ✅ | Regex ASIN/PID extraction, platform detection, image & rating metadata |
| 3 | Review Collection | ✅ | Supports live provider API + demo fallback |
| 4 | NLP Stylistic Pipeline | ✅ | VADER sentiment, exclamation spam, caps detection, marketing phrases |
| 5 | Duplicate Detection | ✅ | Scikit-learn TF-IDF n-gram vectorizer + Cosine Similarity clustering |
| 6 | Supervised ML Model | ✅ | Logistic Regression, Random Forest, Naive Bayes with F1 evaluation |
| 7 | Calibrated 0–100 Risk Score | ✅ | Weighted multi-signal scoring (NLP + Duplicates + ML probability) |
| 8 | Product Trust Dashboard | ✅ | Large Genuine %, Suspicious %, Uncertain % cards, donut & bar charts |
| 9 | Review Explorer | ✅ | Real-time filtering by classification, risk level, search, and sorting |
| 10 | Explainable AI | ✅ | Bulleted, transparent detection reasons per flagged review |
| 11 | Product Comparison | ✅ | Side-by-side metric comparison of 2 products |
| 12 | Downloadable PDF Report | ✅ | ReportLab generated multi-page executive summary |
| 13 | Mobile-Responsive SaaS UI | ✅ | Dark navy aesthetics, Tailwind CSS, Recharts, Framer Motion |

---

## 🤖 6. Model Training & Evaluation

To re-train or evaluate the machine learning models:
```bash
cd backend
python -m app.ml.trainer
```
The system trains **Logistic Regression**, **Random Forest**, and **Multinomial Naive Bayes**, evaluates test-set Precision, Recall, F1-score, and Confusion Matrices, and pickles the best performing model to `app/ml/models/`.

Live metrics are exposed via `/api/model/performance` and visible on the **AI Model** page in the UI.

---

## ⚖️ 7. Ethical AI Compliance & Disclaimer

- A review flagged as *Suspicious* represents statistical anomaly and elevated risk probability, **not** a definitive legal assertion of fraud.
- Product Trust Scores evaluate review authenticity, **not** underlying product engineering or physical durability.
- All demo data is explicitly labelled in the UI with warning badges so judges are never misled.

---
*Built with ❤️ for the College Hackathon.*
