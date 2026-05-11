from fastapi import HTTPException
from sqlalchemy.orm import Session
from dao.employment import (
    get_all_employment,
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


def get_all_service(db: Session, skip: int, limit: int, student_name: str, company_name: str, class_id: int):
    emp_list = get_all_employment(db, skip, limit, student_name, company_name, class_id)
    serialized = [EmploymentResponse.model_validate(item).model_dump() for item in emp_list] if emp_list else []
    return serialized


def get_by_salary_range_service(db: Session, salary_min: int, salary_max: int):
    emp_list = get_by_salary_range(db, salary_min, salary_max)
    return emp_list


def get_statistics_service(db: Session):
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
    emp = get_student_no_by(db, student_no)
    if not emp:
        raise HTTPException(status_code=404, detail="就业信息不存在")
    return emp


def get_employment_id_service(db: Session, employment_id: int):
    return get_employment_id_by(db, employment_id)


def create_employment_service(db: Session, data: EmploymentCreate):
    exist = get_student_no_by(db, data.student_no)
    if exist:
        raise HTTPException(status_code=409, detail="就业信息已存在")
    return create_employment(db, data)


def update_employment_service(db: Session, employment_id: int, data: EmploymentUpdate):
    emp = get_employment_id_by(db, employment_id)
    if not emp:
        raise HTTPException(status_code=404, detail="就业信息不存在")
    update_employment(db, employment_id, data)
    return get_employment_id_by(db, employment_id)


def delete_employment_service(db: Session, employment_id: int):
    emp = get_employment_id_by(db, employment_id)
    if not emp:
        raise HTTPException(status_code=404, detail="就业信息不存在")
    delete_employment(db, employment_id)
    return {"code": 200, "message": "删除成功", "data": employment_id}


def restore_employment_service(db: Session, employment_id: int):
    emp = restore_employment(db, employment_id)
    if not emp:
        raise HTTPException(status_code=404, detail="就业信息不存在，无法恢复")
    return emp
