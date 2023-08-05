from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship

from .database import Base


class SchoolBase(Base):
    __tablename__ = "users_school"

    code = Column(String(100), primary_key=True, nullable=False, unique=True)
    area_code = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)

    users = relationship("User", back_populates="school")


class School(SchoolBase):
    class Config:
        orm_mode = True


class User(Base):
    __tablename__ = "users_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    social_id = Column(String(100))
    password = Column(String(100), nullable=False)
    nickname = Column(String(100))
    school_id = Column(String(100), ForeignKey("users_school.code"))
    is_male = Column(Boolean)
    birthday = Column(Date)
    last_login = Column(DateTime)
    joined_at = Column(DateTime)
    avatar_sgv = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    school = relationship("School", back_populates="users")
