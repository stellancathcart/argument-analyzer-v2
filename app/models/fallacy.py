'''
app/models/fallacy.py
'''
from sqlalchemy import String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Fallacy(Base):
    __tablename__ = "fallacies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    argument_id: Mapped[int] = mapped_column(ForeignKey("arguments.id"), nullable=False)
    fallacy_type: Mapped[str] = mapped_column(String, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    argument: Mapped["Argument"] = relationship(back_populates="fallacies")
