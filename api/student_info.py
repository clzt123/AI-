from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from schemas.student_info import StudentResponse, StudentCreate, StudentUpdate, StudentListResponse
from typing import Optional, Dict, Any, List
from service.student_info import (
    create_student,
    get_students_list,
    check_student_age,
    check_student_gender,
    get_student_by_id,
    update_student_service,
    delete_student_service,
    restore_student_service,
    get_deleted_student_list
)
from service.auth import require_permission, require_login, AuthUser

router = APIRouter(prefix="/students", tags=["学生管理"])

@router.post("/create", response_model=dict)
def create_student_route(student_data: StudentCreate, db: Session = Depends(get_db), _: AuthUser = Depends(require_permission("student_info", "create"))) -> Dict[str, Any]:
    """创建新的学生信息记录"""
    result = create_student(db, student_data)
    return {"code": 200, "message": "添加成功", "data": StudentResponse.model_validate(result).model_dump()}

@router.get("/check", response_model=dict)
def list_students(
    student_name: Optional[str] = None,
    class_id: Optional[int] = None,
    page: int=1, page_size:int=10,
    db: Session=Depends(get_db),
    _: AuthUser = Depends(require_login)
) -> Dict[str, Any]:
    """分页查询学生信息，支持按姓名和班级筛选"""
    total, data = get_students_list(db, student_name, class_id, page, page_size)
    return {"code": 200, "message": "查询成功", "total":total, "data":data, "page":page, "page_size":page_size}

@router.get("/age_stats", response_model=dict)
def get_age_stats(db: Session = Depends(get_db), _: AuthUser = Depends(require_login)) -> Dict[str, Any]:
    """查询年龄超过30岁的学生信息"""
    data = check_student_age(db)
    result = []
    for s in data:
        result.append({
            "id": s.id,
            "student_no": s.student_no,
            "student_name": s.student_name,
            "gender": s.gender,
            "age": s.age,
            "class_id": s.class_id
        })
    return {"code": 200, "message": "查询成功", "data": result}

@router.get("/gender_stats", response_model=dict)
def get_gender_stats(db: Session = Depends(get_db), _: AuthUser = Depends(require_login)) -> Dict[str, Any]:
    """统计每个班级的男女生人数"""
    data = check_student_gender(db)
    return {"code": 200, "message": "查询成功", "data": data}

@router.get("/check/{id}", response_model=dict)
def get_student_by_id_route(id: int, db: Session=Depends(get_db), _: AuthUser = Depends(require_login)) -> Dict[str, Any]:
    """根据ID查询单个学生信息"""
    result = get_student_by_id(db, id)
    return {"code": 200, "message": "查询成功", "data": StudentResponse.model_validate(result).model_dump()}

@router.put("/update/{id}", response_model=dict)
def update_student(id:int, student_data:StudentUpdate, db:Session=Depends(get_db), _: AuthUser = Depends(require_permission("student_info", "update"))) -> Dict[str, Any]:
    """更新指定学生的信息"""
    result = update_student_service(db, id, student_data)
    return {"code": 200, "message": "修改成功", "data": StudentResponse.model_validate(result).model_dump()}

@router.delete("/delete/{id}", response_model=dict)
def delete_student(id:int, db:Session=Depends(get_db), _: AuthUser = Depends(require_permission("student_info", "delete"))) -> Dict[str, Any]:
    """逻辑删除指定学生信息"""
    delete_student_service(db, id)
    return {"code": 200, "message": "删除成功", "data": None}

@router.post("/restore/{id}", response_model=dict)
def restore_student_route(id: int, db:Session=Depends(get_db), _: AuthUser = Depends(require_permission("student_info", "restore"))) -> Dict[str, Any]:
    """恢复已删除的学生信息"""
    restore_student_service(db, id)
    return {"code": 200, "message": "恢复成功", "data": None}

@router.get("/check_is_deleted", response_model=dict)
def check_is_deleted(
    student_name: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    _: AuthUser = Depends(require_login)
) -> Dict[str, Any]:
    """查询已删除的学生列表，支持分页和姓名筛选"""
    total, data = get_deleted_student_list(
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
