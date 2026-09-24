from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DyeLotCreate(BaseModel):
    vat_id: int = Field(..., alias="vatId")
    recipe_name: str = Field(..., min_length=1, max_length=128, alias="recipeName")
    fabric_kg: float = Field(..., gt=0, alias="fabricKg")
    started_at: datetime = Field(..., alias="startedAt")
    operator_name: str = Field(..., min_length=1, max_length=64, alias="operatorName")

    model_config = ConfigDict(populate_by_name=True)


class DyeLotUpdate(BaseModel):
    vat_id: Optional[int] = Field(None, alias="vatId")
    recipe_name: Optional[str] = Field(None, min_length=1, max_length=128, alias="recipeName")
    fabric_kg: Optional[float] = Field(None, gt=0, alias="fabricKg")
    started_at: Optional[datetime] = Field(None, alias="startedAt")
    operator_name: Optional[str] = Field(None, min_length=1, max_length=64, alias="operatorName")

    model_config = ConfigDict(populate_by_name=True)


class DyeLotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    vat_id: int = Field(serialization_alias="vatId")
    recipe_name: str = Field(serialization_alias="recipeName")
    fabric_kg: float = Field(serialization_alias="fabricKg")
    started_at: datetime = Field(serialization_alias="startedAt")
    operator_name: str = Field(serialization_alias="operatorName")
