from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Any, Optional
from dao.employment import (
    get_all_employment,
    count_all_employment,
    get_by_salary_range,
    get_salary_top5,
    get_class_avg,
    get_student_no_by,
    get_employment_id_by,
    create_employment,
    update_employment,
    delete_employment,
    restore_employment
)
from schemas.employment import EmploymentResponse, EmploymentCreate, EmploymentUpdate


def get_all_service(db: Session, page: int, page_size: int, student_name: Optional[str], company_name: Optional[str], class_id: Optional[int]) -> Dict[str, Any]:
    """获取所有就业信息列表，支持分页和多条件筛选"""
    skip = (page - 1) * page_size
    emp_list = get_all_employment(db, skip, page_size, student_name, company_name, class_id)
    total = count_all_employment(db, student_name, company_name, class_id)
    serialized = [EmploymentResponse.model_validate(item).model_dump() for item in emp_list] if emp_list else []
    return {
        "total": total,
        "data": serialized,
        "page": page,
        "page_size": page_size
    }


def get_by_salary_range_service(db: Session, salary_min: int, salary_max: int) -> List:
    """根据薪资范围查询就业信息"""
    emp_list = get_by_salary_range(db, salary_min, salary_max)
    return emp_list


def get_statistics_service(db: Session) -> Dict[str, Any]:
    """获取就业统计数据，包括薪资Top5和班级平均薪资"""
    top5 = get_salary_top5(db)
    class_avg_salary = get_class_avg(db)
    class_result = []
    for item in class_avg_salary:
        class_result.append({
            "class_id": item.class_id,
            "avg_salary": float(item.avg_salary) if item.avg_salary else 0
        })

    return {
        "salary_top5": [EmploymentResponse.model_validate(i).model_dump() for i in top5],
        "class_average_salary": class_result
    }


def get_student_no_service(db: Session, student_no: str):
    """根据学号查询就业信息，不存在则抛出404异常"""
    emp = get_student_no_by(db, student_no)
    if not emp:
        raise HTTPException(status_code=404, detail="就业信息不存在")
    return emp


def get_employment_id_service(db: Session, employment_id: int):
    """根据就业ID查询就业信息"""
    return get_employment_id_by(db, employment_id)


def create_employment_service(db: Session, data: EmploymentCreate):
    """创建新的就业信息记录，学号重复则抛出409异常"""
    exist = get_student_no_by(db, data.student_no)
    if exist:
        raise HTTPException(status_code=409, detail="就业信息已存在")
    try:
        return create_employment(db, data)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="创建就业信息失败")


def update_employment_service(db: Session, employment_id: int, data: EmploymentUpdate):
    """更新指定就业信息记录，不存在则抛出404异常"""
    emp = get_employment_id_by(db, employment_id)
    if not emp:
        raise HTTPException(status_code=404, detail="就业信息不存在")
    update_employment(db, employment_id, data)
    return get_employment_id_by(db, employment_id)


def delete_employment_service(db: Session, employment_id: int) -> Dict[str, Any]:
    """逻辑删除指定就业信息记录，不存在则抛出404异常"""
    emp = get_employment_id_by(db, employment_id)
    if not emp:
        raise HTTPException(status_code=404, detail="就业信息不存在")
    delete_employment(db, employment_id)
    return {"code": 200, "message": "删除成功", "data": employment_id}


def restore_employment_service(db: Session, employment_id: int):
    """恢复已删除的就业信息记录，不存在则抛出404异常"""
    emp = restore_employment(db, employment_id)
    if not emp:
        raise HTTPException(status_code=404, detail="就业信息不存在，无法恢复")
    return emp
