from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.models import StudentList

def get_student_list(db: Session, student_list_id:int):
    student_list = db.query(StudentList).get(student_list_id)
    if not student_list:
        raise HTTPException(status_code=404, detail="요청하신 명렬표가 존재하지 않아요.") 
    return student_list   