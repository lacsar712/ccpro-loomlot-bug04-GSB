from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class FastnessCheckCreate(BaseModel):
    dye_lot_id: int = Field(..., alias="dyeLotId")
    checked_at: datetime = Field(..., alias="checkedAt")
    wash_fastness: int = Field(..., ge=1, le=5, alias="washFastness")
    rub_fastness: float = Field(..., gt=0, alias="rubFastness")
    temp_c: float = Field(..., alias="tempC")
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class FastnessCheckUpdate(BaseModel):
    dye_lot_id: Optional[int] = Field(None, alias="dyeLotId")
    checked_at: Optional[datetime] = Field(None, alias="checkedAt")
    wash_fastness: Optional[int] = Field(None, ge=1, le=5, alias="washFastness")
    rub_fastness: Optional[float] = Field(None, gt=0, alias="rubFastness")
    temp_c: Optional[float] = Field(None, alias="tempC")
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class FastnessCheckOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    dye_lot_id: int = Field(serialization_alias="dyeLotId")
    checked_at: datetime = Field(serialization_alias="checkedAt")
    wash_fastness: int = Field(serialization_alias="washFastness")
    rub_fastness: float = Field(serialization_alias="rubFastness")
    temp_c: float = Field(serialization_alias="tempC")
    notes: Optional[str] = None
