from schemas.teacher import *
from service.teacher import *
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db


router = APIRouter(prefix="/teacher", tags=["老师管理模块"])

@router.get('/all', response_model=list[TeacherResponse])
def get_all_teachers(db: Session = Depends(get_db)):
    teachers = get_all_teachers_list(db)
    return teachers

@router.post('/create', response_model=TeacherResponse)
def add_teacher(t: TeacherCreate, db: Session = Depends(get_db)):
    return create_teacher(db, t)

@router.get('/check',response_model=TeacherListResponse)
def list_teachers(
    teacher_name: Optional[str] = None,
    gender: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    total, data = get_teachers_list(db, teacher_name, gender, page, page_size)
    return {
        "code": 200,
        "message": "查询成功",
        "total": total,
        "data": data,
        "page": page,
        "page_size": page_size
    }

@router.get('/check/{teacher_id}', response_model=TeacherResponse)
def get_teacher_by_id_api(teacher_id: int, db: Session = Depends(get_db)):
    return get_teacher(db, teacher_id)

@router.put('/update/{teacher_id}', response_model=TeacherResponse)
def update_teacher_api(teacher_id: int, data: TeacherUpdate, db: Session = Depends(get_db)):
    return update_teacher_service(db, teacher_id, data)

@router.delete('/delete/{teacher_id}')
def delete_teacher_api(teacher_id: int, db: Session = Depends(get_db)):
    delete_teacher_service(db, teacher_id)
    return {"code": 200, "message": "删除成功", "data": None}

@router.get('/deleted', response_model=TeacherListResponse)
def list_deleted_teachers(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    total, data = get_deleted_teachers_list(db, page, page_size)
    return {
        "code": 200,
        "message": "查询成功",
        "total": total,
        "data": data,
        "page": page,
        "page_size": page_size
    }

@router.put('/restore/{teacher_id}', response_model=TeacherResponse)
def restore_teacher_api(teacher_id: int, db: Session = Depends(get_db)):
    return restore_teacher_service(db, teacher_id)

@router.get('/stats', response_model=TeacherStatsResponse)
def get_stats(db: Session = Depends(get_db)):
    return get_teacher_stats_service(db)
