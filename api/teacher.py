from schemas.teacher import *
from service.teacher import *
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db


router = APIRouter(prefix="/teacher", tags=["老师管理模块"])

#查询所有老师
@router.get('/all', response_model=list[TeacherResponse])
def get_all_teachers(db: Session = Depends(get_db)):
    teachers = judge_get_all_teachers(db)
    return teachers

# 新增老师
@router.post('/create', response_model=TeacherResponse)
def add_teacher(t: TeacherCreate, db: Session = Depends(get_db)):
    return create_teacher(db, t)

# 条件查询（分页）
@router.get('/check',response_model=TeacherListResponse)
def list_teachers(
    teacher_name: Optional[str] = None,
    gender: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    total, data = judge_get_teachers(db, teacher_name, gender, page, page_size)
    return {
        "total": total,
        "data": data,
        "page": page,
        "page_size": page_size
    }

# 单个查询
@router.get('/check/{teacher_id}', response_model=TeacherResponse)
def get_teacher_by_id(teacher_id: int, db: Session = Depends(get_db)):
    return judge_get_teacher(db, teacher_id)

# 修改老师
@router.put('/update/{teacher_id}', response_model=TeacherResponse)
def update_teacher_api(teacher_id: int, data: TeacherUpdate, db: Session = Depends(get_db)):
    return judge_update_teacher(db, teacher_id, data)

# 删除老师
@router.delete('/delete/{teacher_id}')
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    return judge_delete_teacher(db, teacher_id)

# 查询已删除的老师（分页）
@router.get('/deleted', response_model=TeacherListResponse)
def list_deleted_teachers(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    total, data = judge_get_deleted_teachers(db, page, page_size)
    return {
        "total": total,
        "data": data,
        "page": page,
        "page_size": page_size
    }

# 恢复被删除的老师
@router.put('/restore/{teacher_id}', response_model=TeacherResponse)
def restore_teacher_api(teacher_id: int, db: Session = Depends(get_db)):
    return judge_restore_teacher(db, teacher_id)

#统计男女老师人数
@router.get('/stats', response_model=TeacherStatsResponse)
def get_stats(db: Session = Depends(get_db)):
    return judge_get_stats(db)






