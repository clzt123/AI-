from fastapi import HTTPException
from sqlalchemy.orm import Session
from dao.teacher import (
    create_teacher, update_teacher, delete_teacher,
    get_all_teachers, get_teacher_by_id, get_teacher_by_conditions,
    get_deleted_teachers, restore_teacher, get_teacher_stats,
    check_teacher_exists, check_teacher_deleted, check_teacher_exists_any
)
from schemas.teacher import TeacherUpdate

def get_all_teachers_list(db: Session):
    teachers = get_all_teachers(db)
    return teachers if teachers else []

def get_teacher(db: Session, teacher_id: int):
    tea = get_teacher_by_id(db, teacher_id)
    if not tea:
        raise HTTPException(status_code=404, detail="老师不存在")
    return tea

def get_teachers_list(db: Session, teacher_name=None, gender=None, page=1, page_size=10):
    total, data = get_teacher_by_conditions(db, teacher_name, gender, page, page_size)
    return total, data

def get_deleted_teachers_list(db: Session, page=1, page_size=10):
    total, data = get_deleted_teachers(db, page, page_size)
    if total == 0:
        raise HTTPException(status_code=404, detail="未找到已删除的老师")
    return total, data

def update_teacher_service(db: Session, teacher_id: int, data: TeacherUpdate):
    tea = update_teacher(db, teacher_id, data)
    if not tea:
        raise HTTPException(status_code=404, detail="老师不存在")
    return tea

def delete_teacher_service(db: Session, teacher_id: int):
    if not check_teacher_exists_any(db, teacher_id):
        raise HTTPException(status_code=404, detail="老师不存在")
    if check_teacher_deleted(db, teacher_id):
        raise HTTPException(status_code=400, detail="老师已被删除，无需重复删除")
    success = delete_teacher(db, teacher_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除操作失败")
    return {"message": "删除成功"}

def restore_teacher_service(db: Session, teacher_id: int):
    if not check_teacher_deleted(db, teacher_id):
        raise HTTPException(status_code=404, detail="老师不存在或未被删除")

    restored_tea = restore_teacher(db, teacher_id)
    if not restored_tea:
        raise HTTPException(status_code=500, detail="恢复操作失败")
    return restored_tea

def get_teacher_stats_service(db: Session):
    from dao.teacher import get_teacher_stats as dao_get_teacher_stats
    return dao_get_teacher_stats(db)
