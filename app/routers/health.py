from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def root():
    return {"message": "API is online", "status": "healthy"}


@router.get("/health")
def health():
    return {"status": "ok"}
