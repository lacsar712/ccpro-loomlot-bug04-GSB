from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.dye_house import DyeHouse
from app.models.user import User
from app.schemas.dye_house import DyeHouseCreate, DyeHouseUpdate, DyeHouseOut

router = APIRouter(prefix="/api/dye-houses", tags=["dye-houses"])


@router.get("", response_model=List[DyeHouseOut])
def list_dye_houses(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return db.query(DyeHouse).order_by(DyeHouse.id).all()


@router.post("", response_model=DyeHouseOut, status_code=status.HTTP_201_CREATED)
def create_dye_house(
    payload: DyeHouseCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = DyeHouse(
        name=payload.name,
        water_note=payload.water_note,
        notes=payload.notes,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{house_id}", response_model=DyeHouseOut)
def get_dye_house(
    house_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.query(DyeHouse).filter(DyeHouse.id == house_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="染坊不存在")
    return item


@router.put("/{house_id}", response_model=DyeHouseOut)
def update_dye_house(
    house_id: int,
    payload: DyeHouseUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.query(DyeHouse).filter(DyeHouse.id == house_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="染坊不存在")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{house_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dye_house(
    house_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.query(DyeHouse).filter(DyeHouse.id == house_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="染坊不存在")
    db.delete(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="该染坊仍有关联记录，无法删除")
