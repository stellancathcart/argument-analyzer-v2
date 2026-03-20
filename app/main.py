from fastapi import FastAPI
from app.db import Base, engine
from app.routers import health, auth, arguments

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Argument Analyzer",
    description="AI-powered argument analysis using Claude",
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(arguments.router)