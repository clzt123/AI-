from fastapi import HTTPException
from sqlalchemy.orm import Session
from dao import student_info as dao
from schemas.student_info import StudentCreate, StudentResponse, StudentUpdate


def create_student(db: Session, s: StudentCreate):
    return dao.create_student(db, s)

def get_student_by_id(db: Session, id: int):
    stu = dao.get_student(db=db, id=id)
    if not stu:
        raise HTTPException(status_code=404, detail="Student not found")
    return stu

def get_students_list(db: Session, student_name=None, class_id=None, page=1, page_size=10):
    total,data = dao.get_students(db=db, student_name=student_name, class_id=class_id,page=page,page_size=page_size)
    return total,data

def update_student_service(db: Session, id: int, data: StudentUpdate):
    stu = dao.update_student(db=db, id=id, data=data)
    if not stu:
        raise HTTPException(status_code=404, detail="Student not found")
    return stu

def delete_student_service(db: Session, id: int):
    stu = dao.delete_student(db=db, id=id)
    if not stu:
        raise HTTPException(status_code=404, detail="Student not found")
    return stu

def restore_student_service(db: Session, id: int):
    stu = dao.restore_student(db=db, id=id)
    if not stu:
        raise HTTPException(status_code=404, detail="Student not found")
    return stu

def get_deleted_student_list(db: Session, student_name=None,page=1, page_size=10):
    total,data = dao.get_deleted_student(db=db, student_name=student_name, page=page, page_size=page_size)
    return total,data

def check_student_age(db: Session):
    stu = dao.check_student_age(db=db)
    return stu

def check_student_gender(db: Session):
    stu = dao.check_student_gender(db=db)
    return stu
