from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    Table,
)
from sqlalchemy.orm import relationship

from .database import Base


class School(Base):
    __tablename__ = "users_school"

    code = Column(String(10), primary_key=True, nullable=False, unique=True)
    area_code = Column(String(10), nullable=False)
    name = Column(String(10), nullable=False)

    users = relationship("User", back_populates="school")


class User(Base):
    __tablename__ = "users_user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    social_id = Column(String(50))
    password = Column(String(100), nullable=False)
    nickname = Column(String(50))
    school_id = Column(String(10), ForeignKey("users_school.code"))
    is_male = Column(Boolean)
    birthday = Column(Date)
    last_login = Column(DateTime)
    joined_at = Column(DateTime)
    avatar_sgv = Column(String(50))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    school = relationship("School", back_populates="users")
    student_list = relationship("StudentList", back_populates="user")


class StudentList(Base):
    __tablename__ = "users_studentlist"

    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    user_id = Column(Integer, ForeignKey("users_user.id"))
    is_main = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="student_list")
    students = relationship("Student", back_populates="student_list")


student_allergy_table = Table(
    "users_student_allergy",
    Base.metadata,
    Column("student_id", ForeignKey("users_student.id"), primary_key=True),
    Column("allergy_id", ForeignKey("users_allergy.code"), primary_key=True),
)


class Allergy(Base):
    __tablename__ = "users_allergy"

    code = Column(Integer, primary_key=True)
    name = Column(String(20))

    students = relationship(
        "Student", secondary=student_allergy_table, back_populates="allergies"
    )

    def __str__(self):
        return f"Allergy(code={self.code}, name={self.name}, studensts={[student.name for student in self.students]})"


class Student(Base):
    __tablename__ = "users_student"

    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    number = Column(Integer, unique=True)
    is_male = Column(Boolean)
    description = Column(Text, nullable=True)
    list_id = Column(Integer, ForeignKey("users_studentlist.id"))

    student_list = relationship("StudentList", back_populates="students")
    allergies = relationship(
        "Allergy", secondary=student_allergy_table, back_populates="students"
    )

    def __str__(self):
        return f"Student(id={self.id}, name={self.name}, number={self.number}, is_male={self.is_male}, allergies={[allergy.code for allergy in self.allergies]}"
