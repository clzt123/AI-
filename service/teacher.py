from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Tuple, Optional
from dao.teacher import (
    create_teacher, update_teacher, delete_teacher,
    get_all_teachers, get_teacher_by_id, get_teacher_by_conditions,
    get_deleted_teachers, restore_teacher, get_teacher_stats,
    check_teacher_exists, check_teacher_deleted, check_teacher_exists_any
)
from schemas.teacher import TeacherUpdate, TeacherResponse

def get_all_teachers_list(db: Session) -> List[Dict[str, Any]]:
    """获取所有老师信息列表并序列化"""
    teachers = get_all_teachers(db)
    serialized = [TeacherResponse.model_validate(t).model_dump() for t in teachers] if teachers else []
    return serialized

def get_teacher(db: Session, teacher_id: int):
    """根据ID查询老师信息，不存在则抛出404异常"""
    tea = get_teacher_by_id(db, teacher_id)
    if not tea:
        raise HTTPException(status_code=404, detail="老师不存在")
    return tea

def get_teachers_list(db: Session, teacher_name=None, gender=None, page=1, page_size=10) -> Tuple[int, List[Dict[str, Any]]]:
    """分页查询老师信息，支持按姓名和性别筛选"""
    total, data = get_teacher_by_conditions(db, teacher_name, gender, page, page_size)
    serialized_data = [TeacherResponse.model_validate(item).model_dump() for item in data] if data else []
    return total, serialized_data

def get_deleted_teachers_list(db: Session, page=1, page_size=10) -> Tuple[int, List[Dict[str, Any]]]:
    """查询已删除的老师列表，支持分页"""
    total, data = get_deleted_teachers(db, page, page_size)
    if total == 0:
        raise HTTPException(status_code=404, detail="未找到已删除的老师")
    serialized_data = [TeacherResponse.model_validate(item).model_dump() for item in data] if data else []
    return total, serialized_data

def update_teacher_service(db: Session, teacher_id: int, data: TeacherUpdate):
    """更新指定老师的信息，不存在则抛出404异常"""
    tea = update_teacher(db, teacher_id, data)
    if not tea:
        raise HTTPException(status_code=404, detail="老师不存在")
    return tea

def delete_teacher_service(db: Session, teacher_id: int) -> Dict[str, str]:
    """逻辑删除指定老师信息，检查状态并防止重复删除"""
    if not check_teacher_exists_any(db, teacher_id):
        raise HTTPException(status_code=404, detail="老师不存在")
    if check_teacher_deleted(db, teacher_id):
        raise HTTPException(status_code=400, detail="老师已被删除，无需重复删除")
    success = delete_teacher(db, teacher_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除操作失败")
    return {"message": "删除成功"}

def restore_teacher_service(db: Session, teacher_id: int) -> Dict[str, Any]:
    """恢复已删除的老师信息，检查状态并防止无效恢复"""
    if not check_teacher_deleted(db, teacher_id):
        raise HTTPException(status_code=404, detail="老师不存在或未被删除")

    restored_tea = restore_teacher(db, teacher_id)
    if not restored_tea:
        raise HTTPException(status_code=500, detail="恢复操作失败")
    return TeacherResponse.model_validate(restored_tea).model_dump()

def get_teacher_stats_service(db: Session) -> Dict[str, Any]:
    """获取老师性别统计数据"""
    return get_teacher_stats(db)
