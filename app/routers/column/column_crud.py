from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import *

def create_column(db: Session, student_list: StudentList, field = str):
    column = Columns(field = field, student_list = student_list)
    db.add(column)
    db.commit()
    return column

def get_columns(db: Session, studentListId: int):
    columns = db.query(Columns.id, Columns.field).filter(Columns.student_list_id == studentListId).all()
    if not columns:
        raise HTTPException(status_code=404, detail="명렬표가 존재하지 않아요.")    
    return columns
