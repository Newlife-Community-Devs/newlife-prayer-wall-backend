from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str) -> models.User:
    db_user = models.User(
        email=user.email, hashed_password=hashed_password, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_prayer(db: Session, prayer: schemas.PrayerCreate, owner_id: Optional[int] = None) -> models.PrayerRequest:
    """Create a prayer request. For public submissions, pass submitter_name/phone_number/is_anonymous in prayer."""
    db_prayer = models.PrayerRequest(
        title=prayer.title,
        content=prayer.content,
        owner_id=owner_id,
        submitter_name=getattr(prayer, "submitter_name", None),
        phone_number=getattr(prayer, "phone_number", None),
        is_anonymous=getattr(prayer, "is_anonymous", False),
    )
    db.add(db_prayer)
    db.commit()
    db.refresh(db_prayer)
    return db_prayer


def get_prayers_for_user(db: Session, user_id: int):
    return db.query(models.PrayerRequest).filter(models.PrayerRequest.owner_id == user_id).order_by(models.PrayerRequest.created_at.desc()).all()


def get_all_prayers(db: Session):
    return db.query(models.PrayerRequest).order_by(models.PrayerRequest.created_at.desc()).all()


def get_all_prayers_paginated(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    filters: Optional[schemas.PrayerFilter] = None
):
    """Return paginated and filtered prayers with total count"""
    query = db.query(models.PrayerRequest)

    # Apply filters if provided
    if filters:
        if filters.search:
            search = f"%{filters.search}%"
            query = query.filter(
                models.PrayerRequest.content.ilike(search) |
                models.PrayerRequest.title.ilike(search) |
                models.PrayerRequest.submitter_name.ilike(search)
            )
        if filters.is_answered is not None:
            query = query.filter(
                models.PrayerRequest.is_answered == filters.is_answered)
        if filters.is_flagged is not None:
            query = query.filter(
                models.PrayerRequest.is_flagged == filters.is_flagged)
        if filters.status:
            query = query.filter(models.PrayerRequest.status == filters.status)
        if filters.created_after:
            query = query.filter(
                models.PrayerRequest.created_at >= filters.created_after)
        if filters.created_before:
            query = query.filter(
                models.PrayerRequest.created_at <= filters.created_before)

        # Apply sorting
        if filters.sort_by:
            sort_field = getattr(models.PrayerRequest, filters.sort_by.value)
            if filters.sort_order == schemas.SortOrder.DESC:
                sort_field = sort_field.desc()
            query = query.order_by(sort_field)
    else:
        # Default sorting
        query = query.order_by(models.PrayerRequest.created_at.desc())

    total = query.count()
    items = query.offset(skip).limit(limit + 1).all()

    # Check if there are more items
    has_more = len(items) > limit
    items = items[:limit]  # Truncate to requested limit

    return items, total, has_more


def get_prayer(db: Session, prayer_id: int):
    """Get a single prayer request by ID"""
    return db.query(models.PrayerRequest).filter(models.PrayerRequest.id == prayer_id).first()


def update_prayer_status(
    db: Session,
    prayer: models.PrayerRequest,
    update: schemas.PrayerUpdate
):
    """Update prayer request status and flags"""
    if update.is_answered is not None:
        setattr(prayer, "is_answered", update.is_answered)
    if update.is_flagged is not None:
        setattr(prayer, "is_flagged", update.is_flagged)
    if update.status is not None:
        setattr(prayer, "status", update.status)

    db.add(prayer)
    db.commit()
    db.refresh(prayer)
    return prayer


def delete_prayer(db: Session, prayer: models.PrayerRequest):
    db.delete(prayer)
    db.commit()
