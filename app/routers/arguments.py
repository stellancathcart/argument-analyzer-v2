from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User, Argument, Premise, Fallacy
from app.schemas.argument import ArgumentAnalyzeRequest
from app.services.auth_service import decode_access_token
from app.services.claude_service import analyze_argument_with_claude

router = APIRouter(prefix="/arguments", tags=["arguments"])
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials, db: Session) -> User | None:
    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError:
        return None

    email = payload.get("sub")
    if not email:
        return None

    return db.query(User).filter(User.email == email).first()


@router.post("/analyze")
def analyze(
    payload: ArgumentAnalyzeRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    user = get_current_user(credentials, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = analyze_argument_with_claude(payload.text)

    argument = Argument(
        user_id=user.id,
        text=payload.text,
        main_claim=result["main_claim"],
        analysis=result["analysis"],
        argument_strength=result["argument_strength"],
        score=result["score"],
    )
    db.add(argument)
    db.flush()

    for p in result["premises"]:
        db.add(
            Premise(
                argument_id=argument.id,
                text=p["text"],
                premise_type=p["type"],
                order=p["order"],
            )
        )

    for f in result["fallacies"]:
        db.add(
            Fallacy(
                argument_id=argument.id,
                fallacy_type=f["type"],
                explanation=f["explanation"],
                confidence=f["confidence"],
            )
        )

    db.commit()
    db.refresh(argument)

    return {
        "id": argument.id,
        "text": argument.text,
        "main_claim": result["main_claim"],
        "premises": result["premises"],
        "fallacies": result["fallacies"],
        "argument_strength": result["argument_strength"],
        "analysis": result["analysis"],
        "score": result["score"],
    }


@router.get("")
def list_arguments(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    user = get_current_user(credentials, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    arguments = db.query(Argument).filter(Argument.user_id == user.id).all()
    return {
        "total": len(arguments),
        "items": [
            {
                "id": a.id,
                "text": a.text,
                "main_claim": a.main_claim,
                "analysis": a.analysis,
                "argument_strength": a.argument_strength,
                "score": a.score,
                "created_at": a.created_at.isoformat(),
            }
            for a in arguments
        ],
    }