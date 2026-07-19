"""
Seeding endpoint
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from seed_data import seed_all

router = APIRouter()

@router.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    """Endpoint to seed the database with test data"""
    try:
        seed_all(db)
        return {
            "status": "success",
            "message": "Database seeded successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/seed-status")
def seed_status():
    """Check if database has been seeded"""
    return {
        "message": "POST /api/seed to populate database with test data"
    }
