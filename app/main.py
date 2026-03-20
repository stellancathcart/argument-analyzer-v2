import time
from fastapi import FastAPI
from sqlalchemy import text

from app.db import Base, engine
from app.routers import health, auth, arguments


def init_db(retries: int = 10, delay: int = 2):
    for attempt in range(retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            Base.metadata.create_all(bind=engine)
            return
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(delay)


init_db()

app = FastAPI(
    title="Argument Analyzer",
    description="AI-powered argument analysis using Claude",
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(arguments.router)
