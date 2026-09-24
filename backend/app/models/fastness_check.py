from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.dye_lot import DyeLot


class FastnessCheck(Base):
    __tablename__ = "fastness_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    dye_lot_id: Mapped[int] = mapped_column(ForeignKey("dye_lots.id"), nullable=False, index=True)
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    wash_fastness: Mapped[int] = mapped_column(Integer, nullable=False)
    rub_fastness: Mapped[float] = mapped_column(Float, nullable=False)
    temp_c: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    dye_lot: Mapped["DyeLot"] = relationship("DyeLot", back_populates="fastness_checks")
