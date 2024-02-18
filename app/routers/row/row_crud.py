from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import *

def create_row(db: Session, student: Student, column = Columns):
    row = Rows(student= student, column= column)
    db.add(row)
    db.commit()
    return row
