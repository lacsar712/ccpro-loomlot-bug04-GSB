from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.dye_lot import DyeLot
from app.models.user import User
from app.models.vat import Vat
from app.schemas.dye_lot import DyeLotCreate, DyeLotUpdate, DyeLotOut

router = APIRouter(prefix="/api/dye-lots", tags=["dye-lots"])

# 仅就绪 / 染色中的缸可以开立染程；排液缸禁止
OPENABLE_VAT_STATUSES = {"ready", "dyeing"}


def _get_vat_for_update(db: Session, vat_id: int) -> Vat:
    """行锁取缸，保证并发开立时状态校验与回写在同一事务内串行。"""
    return db.query(Vat).filter(Vat.id == vat_id).with_for_update().first()


@router.get("", response_model=List[DyeLotOut])
def list_dye_lots(
    vat_id: Optional[int] = Query(None, alias="vatId"),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    q = db.query(DyeLot)
    if vat_id is not None:
        q = q.filter(DyeLot.vat_id == vat_id)
    return q.order_by(DyeLot.id.desc()).all()


@router.post("", response_model=DyeLotOut, status_code=status.HTTP_201_CREATED)
def create_dye_lot(
    payload: DyeLotCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    # 先做纯输入校验，任何写库之前失败都不得改动缸状态
    recipe_name = (payload.recipe_name or "").strip()
    if not recipe_name:
        raise HTTPException(status_code=400, detail="配方名不能为空")
    operator_name = (payload.operator_name or "").strip()
    if not operator_name:
        raise HTTPException(status_code=400, detail="操作员不能为空")

    try:
        vat = _get_vat_for_update(db, payload.vat_id)
        if not vat:
            raise HTTPException(status_code=400, detail="染缸不存在")
        if vat.status not in OPENABLE_VAT_STATUSES:
            raise HTTPException(
                status_code=409,
                detail=f"染缸状态为「{vat.status}」，仅 ready 或 dyeing 时可新建染程",
            )

        item = DyeLot(
            vat_id=payload.vat_id,
            recipe_name=recipe_name,
            fabric_kg=payload.fabric_kg,
            started_at=payload.started_at,
            operator_name=operator_name,
        )
        db.add(item)
        # 开立与缸状态回写同一事务：同时成功或同时回滚
        vat.status = "dyeing"
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="染程开立失败")
    db.refresh(item)
    return item


@router.get("/{lot_id}", response_model=DyeLotOut)
def get_dye_lot(
    lot_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.query(DyeLot).filter(DyeLot.id == lot_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="染程不存在")
    return item


@router.put("/{lot_id}", response_model=DyeLotOut)
def update_dye_lot(
    lot_id: int,
    payload: DyeLotUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.query(DyeLot).filter(DyeLot.id == lot_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="染程不存在")
    data = payload.model_dump(exclude_unset=True)

    try:
        if "vat_id" in data and data["vat_id"] != item.vat_id:
            vat = _get_vat_for_update(db, data["vat_id"])
            if not vat:
                raise HTTPException(status_code=400, detail="染缸不存在")
            if vat.status not in OPENABLE_VAT_STATUSES:
                raise HTTPException(
                    status_code=409,
                    detail=f"染缸状态为「{vat.status}」，仅 ready 或 dyeing 时可改挂染程",
                )
            # 改挂与缸状态回写同事务
            vat.status = "dyeing"

        for k, v in data.items():
            setattr(item, k, v)
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="染程保存失败")
    db.refresh(item)
    return item


@router.delete("/{lot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dye_lot(
    lot_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    item = db.query(DyeLot).filter(DyeLot.id == lot_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="染程不存在")
    db.delete(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="该染程仍有关联记录，无法删除")
