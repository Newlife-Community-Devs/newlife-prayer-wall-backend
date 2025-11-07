from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    prayers = relationship("PrayerRequest", back_populates="owner")


class PrayerRequest(Base):
    __tablename__ = "prayer_requests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_answered = Column(Boolean, default=False)
    is_flagged = Column(Boolean, default=False)
    # pending, approved, rejected, archived
    status = Column(String, default="pending")
    # Optional submitter details for public submissions
    submitter_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    is_anonymous = Column(Boolean, default=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    owner = relationship("User", back_populates="prayers")
