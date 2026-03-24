'''
app/routers/health.py
'''

from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.db import engine

router = APIRouter(tags=["health"])


@router.get("/")
def root():
    return {"message": "API is online", "status": "healthy"}


@router.get("/health")
def health():
    return {"status": "healthy"}

@router.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return {"status": "healthy", "database": "reachable"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={"status": "unhealthy", "database": "unreachable", "error": str(e)},
        )

# Health test(s)

def test_health_db_returns_200():
    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["database"] == "reachable"
