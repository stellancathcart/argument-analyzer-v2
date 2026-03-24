'''
app/models/premise.py
'''
from sqlalchemy import Text, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base

class Premise(Base):
    __tablename__ = "premises"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    argument_id: Mapped[int] = mapped_column(ForeignKey("arguments.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    premise_type: Mapped[str] = mapped_column(String, default="supporting")
    order: Mapped[int] = mapped_column(default=0)

    argument: Mapped["Argument"] = relationship(back_populates="premises")
