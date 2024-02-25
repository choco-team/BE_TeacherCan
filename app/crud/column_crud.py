from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import *
from app.schemas import column_schema


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

def update_column(db: Session, column_update: column_schema.ColumnWithId):
    column = read_column_by_id(db = db, column_id = column_update.id)
    column.field = column_update.field
    db.commit()
    return column

def delete_column(db: Session, column_id: int):
    q= read_column_by_id(db = db, column_id = column_id)
    print(q)
    db.delete(q)
    db.commit()



# def get_column(db: Session, column: schemas.ColumnCreate):
#     stmt = (
#         select(models.Columns)
#         .where(models.Columns.field == column.field)
#         .where(
#             or_(
#                 models.Columns.student_list_id == column.student_list_id,
#                 models.Columns.student_id.in_(column.student_id),
#             )
#         )
#         .order_by(models.Columns.id)
#     )
#     columns = db.scalars(stmt).all()
#     return columns


# def create_column(db: Session, email: str, column: schemas.ColumnCreate):
#     db_column = models.Columns(
#         field=column.field,
#         student_list_id=column.student_list_id,
#     )
#     db.add(db_column)
#     for id in column.student_id:
#         db.add(
#             models.Columns(
#                 field=column.field,
#                 student_id=id,
#             )
#         )

#     db.commit()
#     db.refresh(db_column)
#     return get_student_list(db, email, column.student_list_id)


# def update_column(db: Session, column: schemas.ColumnUpdate, email: str):
#     print(column)
#     columns = get_column(db, column)
#     for col, val in zip(columns[1:], column.value):
#         col.value = val
#     db.flush()
#     db.commit()
#     return get_student_list(db, email, column.student_list_id)
