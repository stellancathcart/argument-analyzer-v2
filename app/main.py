'''
app/services/main.py
'''

import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Argument Analyzer",
    description="AI-powered argument analysis using Claude",
    lifespan=lifespan,
)

logger = logging.getLogger("uvicorn.error")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    logger.info(
        f"[{request_id}] Started {request.method} {request.url.path}"
    )

    try:
        response = await call_next(request)
    except Exception:
        duration = time.perf_counter() - start
        logger.exception(
            f"[{request_id}] Failed {request.method} {request.url.path} in {duration:.4f}s"
        )
        raise

    duration = time.perf_counter() - start
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{duration:.4f}"

    logger.info(
        f"[{request_id}] Completed {request.method} {request.url.path} "
        f"with {response.status_code} in {duration:.4f}s"
    )

    return response

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(arguments.router)
