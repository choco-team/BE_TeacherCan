from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship

from .database import Base


class SchoolBase(Base):
    __tablename__ = "users_school"

    code = Column(String, primary_key=True, nullable=False, unique=True)
    area_code = Column(String, nullable=False)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="school")


class School(SchoolBase):
    class Config:
        orm_mode = True


class User(Base):
    __tablename__ = "users_user"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False, unique=True, index=True)
    social_id = Column(String)
    password = Column(String, nullable=False)
    email = Column(String, unique=True)
    nickname = Column(String)
    school_id = Column(String, ForeignKey("users_school.code"))
    is_male = Column(Boolean)
    birthday = Column(Date)
    last_login = Column(DateTime)
    joined_at = Column(DateTime)
    avatar_sgv = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    school = relationship("School", back_populates="users")
