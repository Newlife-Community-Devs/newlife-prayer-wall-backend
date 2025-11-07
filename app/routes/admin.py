from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Tuple
from .. import schemas, crud
from ..database import get_db
from ..auth import require_admin

router = APIRouter()


@router.get("/prayers", response_model=schemas.PrayerListOut)
def list_all_prayers(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200),
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Return paginated list of prayer requests for admins.

    Response includes `items` and `total`.
    """
    skip = (page - 1) * page_size
    items, total = crud.get_all_prayers_paginated(
        db, skip=skip, limit=page_size)
    return {"items": items, "total": total}


@router.patch("/prayers/{prayer_id}/answered", response_model=schemas.PrayerOut)
def mark_answered(prayer_id: int, answered: bool = True, db: Session = Depends(get_db), admin=Depends(require_admin)):
    prayer = crud.get_prayer(db, prayer_id)
    if not prayer:
        raise HTTPException(status_code=404, detail="Prayer not found")
    return crud.mark_prayer_answered(db, prayer, answered=answered)


@router.delete("/prayers/{prayer_id}")
def delete_prayer(prayer_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    prayer = crud.get_prayer(db, prayer_id)
    if not prayer:
        raise HTTPException(status_code=404, detail="Prayer not found")
    crud.delete_prayer(db, prayer)
    return {"detail": "Prayer deleted"}
