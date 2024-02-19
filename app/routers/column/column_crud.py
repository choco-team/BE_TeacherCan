from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import *
from app.routers.column.column_schema import *


def create_column(db: Session, student_list: StudentList, field=str):
    column = Columns(field=field, student_list=student_list)
    db.add(column)
    db.commit()
    return column

def read_column_list(db: Session, studentListId: int):
    columns = db.query(Columns).filter(Columns.student_list_id == studentListId).all()
    if not columns:
        raise HTTPException(status_code=404, detail="column이 존재하지 않아요.")    
    return columns

def read_column_by_id(db: Session, column_id: int):
    column = db.query(Columns).get(column_id)
    if not column:
        raise HTTPException(status_code=404, detail="column이 존재하지 않아요.")    
    return column

def update_column(db: Session, column_update: ColumnWithId):
    column = read_column_by_id(db = db, column_id = column_update.id)
    column.field = column_update.field
    db.commit()
    return column

def delete_column(db: Session, column_id: int):
    q= read_column_by_id(db = db, column_id = column_id)
    print(q)
    db.delete(q)
    db.commit()