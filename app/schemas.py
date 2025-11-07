from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PrayerStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class PrayerSortField(str, Enum):
    CREATED_AT = "created_at"
    IS_ANSWERED = "is_answered"
    IS_FLAGGED = "is_flagged"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True


class PrayerCreate(BaseModel):
    title: Optional[str] = None
    content: str
    # optional public submission fields
    submitter_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_anonymous: Optional[bool] = False


class PrayerOut(BaseModel):
    id: int
    title: Optional[str]
    content: str
    created_at: datetime
    is_answered: bool
    is_flagged: bool
    owner_id: Optional[int]
    submitter_name: Optional[str]
    phone_number: Optional[str]
    is_anonymous: Optional[bool]

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class PrayerPublicIn(BaseModel):
    # matches frontend keys
    name: Optional[str] = None
    phoneNumber: Optional[str] = None
    prayerRequest: str
    keepAnonymous: Optional[bool] = False


class PrayerListOut(BaseModel):
    items: list[PrayerOut]
    total: int
    has_more: bool

    class Config:
        orm_mode = True


class PrayerUpdate(BaseModel):
    is_answered: Optional[bool] = None
    is_flagged: Optional[bool] = None
    status: Optional[PrayerStatus] = None


class PrayerFilter(BaseModel):
    search: Optional[str] = None
    is_answered: Optional[bool] = None
    is_flagged: Optional[bool] = None
    status: Optional[PrayerStatus] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    sort_by: Optional[PrayerSortField] = PrayerSortField.CREATED_AT
    sort_order: Optional[SortOrder] = SortOrder.DESC
