from fastapi import APIRouter
from ...services.ml_classifier import MLClassifier

router = APIRouter()

@router.get("/performance")
async def get_model_performance():
    clf = MLClassifier()
    return clf.get_model_info()
