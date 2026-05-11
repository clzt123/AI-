from schemas.teacher import TeacherCreate, TeacherUpdate, TeacherListResponse, TeacherResponse, TeacherStatsResponse
from service.teacher import (
    get_all_teachers_list,
    create_teacher,
    get_teachers_list,
    get_teacher,
    update_teacher_service,
    delete_teacher_service,
    get_deleted_teachers_list,
    restore_teacher_service,
    get_teacher_stats_service
)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, Tuple, List
from database import get_db


router = APIRouter(prefix="/teachers", tags=["老师管理模块"])

@router.get('/all', response_model=dict)
def get_all_teachers(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """获取所有老师信息列表"""
    teachers = get_all_teachers_list(db)
    return {"code": 200, "message": "查询成功", "data": teachers}

@router.post('/create', response_model=dict)
def add_teacher(t: TeacherCreate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """创建新的老师信息记录"""
    result = create_teacher(db, t)
    return {"code": 200, "message": "添加成功", "data": TeacherResponse.model_validate(result).model_dump()}

@router.get('/check', response_model=dict)
def list_teachers(
    teacher_name: Optional[str] = None,
    gender: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """分页查询老师信息，支持按姓名和性别筛选"""
    total, data = get_teachers_list(db, teacher_name, gender, page, page_size)
    return {
        "code": 200,
        "message": "查询成功",
        "total": total,
        "data": data,
        "page": page,
        "page_size": page_size
    }

@router.get('/check/{teacher_id}', response_model=dict)
def get_teacher_by_id(teacher_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """根据ID查询单个老师信息"""
    result = get_teacher(db, teacher_id)
    return {"code": 200, "message": "查询成功", "data": TeacherResponse.model_validate(result).model_dump()}

@router.put('/update/{teacher_id}', response_model=dict)
def update_teacher(teacher_id: int, data: TeacherUpdate, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """更新指定老师的信息"""
    result = update_teacher_service(db, teacher_id, data)
    return {"code": 200, "message": "修改成功", "data": TeacherResponse.model_validate(result).model_dump()}

@router.delete('/delete/{teacher_id}', response_model=dict)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """逻辑删除指定老师信息"""
    delete_teacher_service(db, teacher_id)
    return {"code": 200, "message": "删除成功", "data": None}

@router.get('/deleted', response_model=dict)
def list_deleted_teachers(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """查询已删除的老师列表，支持分页"""
    total, data = get_deleted_teachers_list(db, page, page_size)
    return {
        "code": 200,
        "message": "查询成功",
        "total": total,
        "data": data,
        "page": page,
        "page_size": page_size
    }

@router.put('/restore/{teacher_id}', response_model=dict)
def restore_teacher(teacher_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """恢复已删除的老师信息"""
    return {"code": 200, "message": "恢复成功", "data": restore_teacher_service(db, teacher_id)}

@router.get('/stats', response_model=dict)
def get_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """获取老师性别统计数据"""
    return {"code": 200, "message": "查询成功", "data": get_teacher_stats_service(db)}
