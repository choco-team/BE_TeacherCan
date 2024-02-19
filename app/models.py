from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

class Gender(str, Enum):
    남 = "남"
    여 = "여"


class School(Base):
    __tablename__ = "school"

    code = Column(String(10), primary_key=True, nullable=False, unique=True)
    area_code = Column(String(10), nullable=False)
    name = Column(String(10), nullable=False)

    users = relationship("User", back_populates="school")

    def __repr__(self):
        return f"School(name={self.name})"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    social_id = Column(String(50))
    password = Column(String(100), nullable=False)
    nickname = Column(String(50))
    school_id = Column(String(10), ForeignKey("school.code"))
    gender = Column(String(10))
    birthday = Column(Date)
    last_login = Column(DateTime)
    joined_at = Column(DateTime, default=func.now())
    avatar_sgv = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    school = relationship("School", back_populates="users")
    student_list = relationship("StudentList", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(email={self.email}, nickname={self.nickname}, school={self.school}, student_list={self.student_list})"


class StudentList(Base):
    __tablename__ = "student_list"

    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    user_id = Column(Integer, ForeignKey("user.id"))
    is_main = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    has_allergy = Column(Boolean, default=False)

    user = relationship("User", back_populates="student_list")
    columns = relationship(
        "Columns", back_populates="student_list", cascade="all, delete-orphan"
    )
    students = relationship(
        "Student", back_populates="student_list", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"StudentList(name={self.name}, is_main={self.is_main}), students={self.students}"


student_allergy_table = Table(
    "student_allergy_set",
    Base.metadata,
    Column("student_id", ForeignKey("student.id"), primary_key=True),
    Column("allergy_id", ForeignKey("allergy.code"), primary_key=True),
)


class Allergy(Base):
    __tablename__ = "allergy"

    code = Column(Integer, primary_key=True)
    name = Column(String(20))

    students = relationship(
        "Student", secondary=student_allergy_table, back_populates="allergy"
    )

    def __repr__(self):
        return f"Allergy(code={self.code}, name={self.name}, studensts={[student.name for student in self.students]})"


class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    number = Column(Integer)
    gender = Column(String(10))
    list_id = Column(Integer, ForeignKey("student_list.id"))

    student_list = relationship("StudentList", back_populates="students")
    allergy = relationship(
        "Allergy",
        secondary=student_allergy_table,
        back_populates="students",
    )
    rows = relationship("Rows", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Student(id={self.id}, name={self.name}, number={self.number}, gender={self.gender}, allergy={[allergy.code for allergy in self.allergy]}"


class Columns(Base):
    __tablename__ = "student_list_column"

    id = Column(Integer, primary_key=True)
    field = Column(String(20))
    student_list_id = Column(Integer, ForeignKey("student_list.id"))

    student_list = relationship("StudentList", back_populates="columns")
    rows = relationship("Rows", back_populates="column", cascade="all, delete-orphan")

    def __repr__(self):
        return f"{self.id}"


class Rows(Base):
    __tablename__ = "student_list_row"

    id = Column(Integer, primary_key=True)
    value = Column(String(100))

    column_id = Column(
        Integer, ForeignKey("student_list_column.id")
    )
    student_id = Column(Integer, ForeignKey("student.id"))

    column = relationship("Columns", back_populates="rows")
    student = relationship("Student", back_populates="rows")
