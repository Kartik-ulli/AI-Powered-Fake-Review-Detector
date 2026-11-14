from fastapi import APIRouter
from ...demo.sample_data import DemoData

router = APIRouter()

@router.get("/products")
async def get_demo_products():
    """List available demo products for hackathon demonstration."""
    return {
        "demo_products": DemoData.get_all_demo_products(),
        "note": "These are simulated datasets for demonstration purposes only. They do not represent real product reviews."
    }
