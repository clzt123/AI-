from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas.student_info import *
from typing import Optional
from service.student_info import *

router = APIRouter(prefix="/students", tags=["学生管理"])

@router.post("/create", response_model=StudentResponse)
def create_student_api(s: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db, s)

@router.get("/check", response_model=StudentListResponse)
def list_students(
    student_name: Optional[str] = None,
    class_id: Optional[int] = None,
    page: int=1, page_size:int=10,
    db: Session=Depends(get_db)
):
    total, data = judge_get_students(db, student_name, class_id, page, page_size)
    return {"code": 200, "message": "查询成功", "total":total, "data":data, "page":page, "page_size":page_size}

@router.get("/age_stats", response_model=List[StudentResponse])
def get_age_stats(db: Session = Depends(get_db)):
    return judge_check_student_age(db)

@router.get("/gender_stats")
def get_gender_stats(db: Session = Depends(get_db)):
    return judge_check_student_gender(db)

@router.get("/check/{id}", response_model=StudentResponse)
def get_student_by_id(id: int, db: Session=Depends(get_db)):
    return judge_get_student(db, id)

@router.put("/update/{id}", response_model=StudentResponse)
def update_student(id:int, s:StudentUpdate, db:Session=Depends(get_db)):
    return judge_update_student(db, id, s)

@router.delete("/delete/{id}")
def delete_student(id:int, db:Session=Depends(get_db)):
    judge_delete_student(db, id)
    return {"code": 200, "message": "删除成功", "data": None}

@router.put("/restore/{id}")
def restore_api(id: int, db:Session=Depends(get_db)):
    judge_restore_student(db, id)
    return {"code": 200, "message": "恢复成功", "data": None}

@router.get("/check_is_deleted", response_model=StudentListResponse)
def check_is_deleted(
    student_name: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    total, data = judge_get_deleted_student(
        db=db,
        student_name=student_name,
        page=page,
        page_size=page_size
    )
    return {
        "code": 200,
        "message": "查询成功",
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": data
    }
