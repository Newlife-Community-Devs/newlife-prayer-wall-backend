from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db
from ..auth import get_current_active_user

router = APIRouter()


@router.post("/", response_model=schemas.PrayerOut)
def create_prayer(prayer_in: schemas.PrayerCreate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    prayer = crud.create_prayer(db, prayer_in, owner_id=current_user.id)
    return prayer


@router.post("/submit", response_model=schemas.PrayerOut, status_code=201)
def submit_prayer_public(payload: schemas.PrayerPublicIn, db: Session = Depends(get_db)):
    """Public endpoint for submitting prayer requests from the frontend modal.

    Maps frontend field names to the internal schema and stores the submitter info
    only when the user does not choose to remain anonymous.
    """
    # Map frontend payload to internal PrayerCreate
    content = payload.prayerRequest
    is_anonymous = bool(payload.keepAnonymous)
    submitter_name = None if is_anonymous else payload.name
    phone_number = None if is_anonymous else payload.phoneNumber

    prayer_in = schemas.PrayerCreate(
        title=None,
        content=content,
        submitter_name=submitter_name,
        phone_number=phone_number,
        is_anonymous=is_anonymous,
    )

    prayer = crud.create_prayer(db, prayer_in, owner_id=None)
    return prayer


@router.get("/", response_model=List[schemas.PrayerOut])
def list_my_prayers(db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return crud.get_prayers_for_user(db, user_id=current_user.id)


@router.get("/wall", response_model=schemas.PrayerListOut)
def get_prayer_wall(
    skip: int = 0,
    limit: int = 20,
    filters: schemas.PrayerFilter = Depends(),
    db: Session = Depends(get_db)
):
    """Get paginated and filtered public prayer wall"""
    items, total, has_more = crud.get_all_prayers_paginated(
        db, 
        skip=skip, 
        limit=limit, 
        filters=filters
    )
    return {
        "items": items,
        "total": total,
        "has_more": has_more
    }


@router.patch("/{prayer_id}", response_model=schemas.PrayerOut)
def update_prayer(
    prayer_id: int,
    update: schemas.PrayerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Update prayer status (admin only)"""
    prayer = crud.get_prayer(db, prayer_id)
    if not prayer:
        raise HTTPException(status_code=404, detail="Prayer request not found")
    
    # Only admins can update any prayer request
    if not current_user.is_admin and prayer.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this prayer request")
    
    # Regular users can only mark their own prayers as answered
    if not current_user.is_admin:
        if update.status or update.is_flagged:
            raise HTTPException(status_code=403, detail="Only admins can update status or flag prayers")
    
    return crud.update_prayer_status(db, prayer, update)


@router.get("/moderation", response_model=schemas.PrayerListOut)
def get_prayers_for_moderation(
    skip: int = 0,
    limit: int = 20,
    filters: schemas.PrayerFilter = Depends(),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Get prayers needing moderation (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to access moderation queue")
    
    # Default to showing pending prayers if no status filter
    if not filters.status:
        filters.status = schemas.PrayerStatus.PENDING
    
    items, total, has_more = crud.get_all_prayers_paginated(
        db, 
        skip=skip, 
        limit=limit, 
        filters=filters
    )
    return {
        "items": items,
        "total": total,
        "has_more": has_more
    }
