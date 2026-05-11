from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from schemas.employment import EmploymentResponse, EmploymentCreate, EmploymentUpdate
from service.employment import (
    get_all_service,
    get_by_salary_range_service,
    get_statistics_service,
    create_employment_service,
    get_student_no_service,
    update_employment_service,
    delete_employment_service,
    restore_employment_service
)
from database import get_db

router = APIRouter(prefix="/employments", tags=["就业管理"])


@router.get("/all", response_model=dict)
def get_all_api(
        page: int = Query(1, description="页码", ge=1),
        page_size: int = Query(10, description="每页条数", ge=1, le=50),
        student_name: str = Query(None, description="学生姓名"),
        company_name: str = Query(None, description="就业公司"),
        class_id: int = Query(None, description="班级ID"),
        db: Session = Depends(get_db)
):
    skip = (page - 1) * page_size
    emp_list = get_all_service(db, skip, page_size, student_name, company_name, class_id)
    return {"code": 200,
            "message": "查询成功",
            "data": emp_list}


@router.get("/salary/range", response_model=dict)
def get_emp_by_salary_range(
    salary_min: int = Query(..., description="最低薪资"),
    salary_max: int = Query(..., description="最高薪资"),
    db: Session = Depends(get_db)
):
    emp_list = get_by_salary_range_service(db, salary_min, salary_max)
    return {
        "code": 200,
        "message": "查询成功",
        "data": [EmploymentResponse.model_validate(item).model_dump() for item in emp_list]
    }


@router.get("/statistics", response_model=dict)
def get_employment_statistics(db: Session = Depends(get_db)):
    data = get_statistics_service(db)
    return {
        "code": 200,
        "message": "统计成功",
        "data": data
    }


@router.post("/", response_model=dict)
def create_employment_api(data: EmploymentCreate, db: Session = Depends(get_db)):
    emp = create_employment_service(db, data)
    return {"code": 200,
            "message": "添加成功",
            "data": EmploymentResponse.model_validate(emp).model_dump()}


@router.get("/{student_no}", response_model=dict)
def get_student_no_api(student_no: str, db: Session = Depends(get_db)):
    emp = get_student_no_service(db, student_no)
    return {"code": 200,
            "message": "查询成功",
            "data": EmploymentResponse.model_validate(emp).model_dump()}


@router.put("/{employment_id}", response_model=dict)
def update_employment_api(employment_id: int, data: EmploymentUpdate, db: Session = Depends(get_db)):
    emp = update_employment_service(db, employment_id, data)
    return {"code": 200,
            "message": "修改成功",
            "data": EmploymentResponse.model_validate(emp).model_dump()}


@router.delete("/{employment_id}", response_model=dict)
def delete_employment_api(employment_id: int, db: Session = Depends(get_db)):
    delete_employment_service(db, employment_id)
    return {"code": 200,
            "message": "删除成功",
            "data": None}


@router.put("/restore/{employment_id}", response_model=dict)
def restore_employment_api(employment_id: int, db: Session = Depends(get_db)):
    restore_employment_service(db, employment_id)
    return {
        "code": 200,
        "message": "恢复成功",
        "data": None
    }
