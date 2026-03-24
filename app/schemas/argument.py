from pydantic import BaseModel


class ArgumentAnalyzeRequest(BaseModel):
    text: str


class PremiseOut(BaseModel):
    text: str
    type: str
    order: int


class FallacyOut(BaseModel):
    type: str
    explanation: str
    confidence: float


class ArgumentResponse(BaseModel):
    id: int
    text: str
    main_claim: str
    premises: list[PremiseOut]
    fallacies: list[FallacyOut]
    argument_strength: str
    analysis: str
    score: float

    # Additional metadata
    model_name: str | None = None
    prompt_version: str | None = None
    latency_ms: float | None = None
    analysis_status: str
    error_type: str | None = None