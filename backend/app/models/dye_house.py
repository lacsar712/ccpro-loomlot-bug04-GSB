from typing import List, TYPE_CHECKING

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.vat import Vat


class DyeHouse(Base):
    __tablename__ = "dye_houses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    water_note: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    vats: Mapped[List["Vat"]] = relationship(
        "Vat", back_populates="dye_house", cascade="all, delete-orphan"
    )
