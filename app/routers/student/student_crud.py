from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import *

def get_student(db: Session, studentListId:int):
    students = db.query(Student).filter(Student.list_id == studentListId).all()
    if not students:
        raise HTTPException(status_code=404, detail="학생이 존재하지 않아요.")    
    return students