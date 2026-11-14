from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .config import settings
from .database import create_tables
from .api.routes import products, analysis, reviews, comparison, reports

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting TrustScope AI backend...")
    create_tables()
    try:
        import nltk
        for resource in ['punkt', 'stopwords', 'vader_lexicon', 'averaged_perceptron_tagger', 'punkt_tab']:
            try:
                nltk.download(resource, quiet=True)
            except Exception:
                pass
    except Exception as e:
        logger.warning(f"NLTK init warning: {e}")
    logger.info("TrustScope AI backend ready.")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="TrustScope AI API",
    description="AI-powered fake product review detection",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["reviews"])
app.include_router(comparison.router, prefix="/api/comparison", tags=["comparison"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])

# Import demo and model routes after they exist
try:
    from .api.routes import demo
    app.include_router(demo.router, prefix="/api/demo", tags=["demo"])
except ImportError:
    pass

try:
    from .api.routes import model_info
    app.include_router(model_info.router, prefix="/api/model", tags=["model"])
except ImportError:
    pass

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "TrustScope AI", "version": "1.0.0"}

# Serve frontend build if available
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "TrustScope AI API", "docs": "/docs"}
