from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Tuple
from .. import schemas, crud
from ..database import get_db
from ..auth import require_admin

router = APIRouter()


@router.get("/prayers")
def list_all_prayers(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=200),
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """Return paginated list of prayer requests for admins.

    Response includes pagination metadata and prayer data.
    """
    skip = (page - 1) * page_size
    items, total, has_more = crud.get_all_prayers_paginated(
        db, skip=skip, limit=page_size)

    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    lower_bound = skip + 1 if total > 0 else 0
    upper_bound = min(skip + page_size, total)

    return {
        "message": "Success",
        "code": 200,
        "data": {
            "page": page,
            "pageSize": page_size,
            "totalRecords": total,
            "lowerBoundSize": lower_bound,
            "upperBoundSize": upper_bound,
            "totalPages": total_pages,
            "data": items
        }
    }


@router.patch("/prayers/{prayer_id}/approve", response_model=schemas.PrayerOut)
def approve_prayer(prayer_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    """Approve a prayer request (set status to 'approved')"""
    prayer = crud.get_prayer(db, prayer_id)
    if not prayer:
        raise HTTPException(status_code=404, detail="Prayer not found")
    prayer.status = "approved"
    db.commit()
    db.refresh(prayer)
    return prayer


@router.patch("/prayers/{prayer_id}/answered", response_model=schemas.PrayerOut)
def mark_answered(prayer_id: int, answered: bool = True, db: Session = Depends(get_db), admin=Depends(require_admin)):
    """Mark a prayer request as answered"""
    prayer = crud.get_prayer(db, prayer_id)
    if not prayer:
        raise HTTPException(status_code=404, detail="Prayer not found")
    prayer.is_answered = answered
    db.commit()
    db.refresh(prayer)
    return prayer


@router.delete("/prayers/{prayer_id}")
def delete_prayer(prayer_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    prayer = crud.get_prayer(db, prayer_id)
    if not prayer:
        raise HTTPException(status_code=404, detail="Prayer not found")
    crud.delete_prayer(db, prayer)
    return {"detail": "Prayer deleted"}
