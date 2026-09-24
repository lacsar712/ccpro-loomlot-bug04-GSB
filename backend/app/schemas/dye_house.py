from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DyeHouseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=128)
    water_note: str = Field(..., min_length=1, max_length=255, alias="waterNote")
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class DyeHouseUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=128)
    water_note: Optional[str] = Field(None, min_length=1, max_length=255, alias="waterNote")
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)


class DyeHouseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    name: str
    water_note: str = Field(serialization_alias="waterNote")
    notes: Optional[str] = None
