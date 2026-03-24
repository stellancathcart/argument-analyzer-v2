from datetime import datetime
from sqlalchemy import Text, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Argument(Base):
    __tablename__ = "arguments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    main_claim: Mapped[str | None] = mapped_column(Text, nullable=True)
    analysis: Mapped[str | None] = mapped_column(Text, nullable=True)
    argument_strength: Mapped[str | None] = mapped_column(Text, nullable=True)
    score: Mapped[float | None] = mapped_column(nullable=True)

    model_name: Mapped[str | None] = mapped_column(String, nullable=True)
    prompt_version: Mapped[str | None] = mapped_column(String, nullable=True)
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    analysis_status: Mapped[str] = mapped_column(String, default="success", nullable=False)
    error_type: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship(back_populates="arguments")
    premises: Mapped[list["Premise"]] = relationship(
        back_populates="argument",
        cascade="all, delete-orphan",
    )
    fallacies: Mapped[list["Fallacy"]] = relationship(
        back_populates="argument",
        cascade="all, delete-orphan",
    )