from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Any, Tuple, Optional
from dao import student_info as dao
from schemas.student_info import StudentCreate, StudentResponse, StudentUpdate


def create_student(db: Session, s: StudentCreate):
    """创建新的学生信息记录"""
    try:
        return dao.create_student(db, s)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="创建学生失败，可能学号已存在")

def get_student_by_id(db: Session, id: int):
    """根据ID查询学生信息，不存在则抛出404异常"""
    stu = dao.get_student(db=db, id=id)
    if not stu:
        raise HTTPException(status_code=404, detail="学生不存在")
    return stu

def get_students_list(db: Session, student_name=None, class_id=None, page=1, page_size=10) -> Tuple[int, List[Dict[str, Any]]]:
    """分页查询学生信息，支持按姓名和班级筛选"""
    total, data = dao.get_students(db=db, student_name=student_name, class_id=class_id, page=page, page_size=page_size)
    serialized_data = [StudentResponse.model_validate(item).model_dump() for item in data] if data else []
    return total, serialized_data

def update_student_service(db: Session, id: int, data: StudentUpdate):
    """更新指定学生的信息，不存在则抛出404异常"""
    stu = dao.update_student(db=db, id=id, data=data)
    if not stu:
        raise HTTPException(status_code=404, detail="学生不存在")
    return stu

def delete_student_service(db: Session, id: int):
    """逻辑删除指定学生信息，不存在则抛出404异常"""
    stu = dao.delete_student(db=db, id=id)
    if not stu:
        raise HTTPException(status_code=404, detail="学生不存在")
    return stu

def restore_student_service(db: Session, id: int):
    """恢复已删除的学生信息，不存在则抛出404异常"""
    stu = dao.restore_student(db=db, id=id)
    if not stu:
        raise HTTPException(status_code=404, detail="学生不存在")
    return stu

def get_deleted_student_list(db: Session, student_name=None, page=1, page_size=10) -> Tuple[int, List[Dict[str, Any]]]:
    """查询已删除的学生列表，支持分页和姓名筛选"""
    total, data = dao.get_deleted_student(db=db, student_name=student_name, page=page, page_size=page_size)
    serialized_data = [StudentResponse.model_validate(item).model_dump() for item in data] if data else []
    return total, serialized_data

def check_student_age(db: Session) -> List:
    """查询年龄超过30岁的学生信息"""
    stu = dao.check_student_age(db=db)
    return stu

def check_student_gender(db: Session) -> List:
    """统计每个班级的男女生人数"""
    stu = dao.check_student_gender(db=db)
    return stu
