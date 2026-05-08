from fastapi import APIRouter,Query,Depends
from sqlalchemy.orm import Session
from service.student_service import *
from schemas.student_schemas import *
from database import get_db

router = APIRouter(prefix="/students2", tags=["学生管理2"])

#新增学生
@router.post("/student_create/", response_model=StudentResponse)
def create_student(
        student:StudentCreate,
        db: Session = Depends(get_db)
):
    return create_student_service(db,student)

#删除学生信息
@router.delete("/student_delete/{student_id}")
def delete_student(
        student_id:int,
        db: Session = Depends(get_db)
):
    delete_student_service(db,student_id)
    return {"code": 200, "message": "删除成功", "data": None}

#修改学生信息
@router.put("/student_update/{student_id}",response_model=StudentResponse)
def update_student(
        student_id:int,
        student:StudentUpdate,
        db: Session = Depends(get_db)
):
    return update_student_service(db,student_id,student)

#查询单个学生
@router.get("/student_get/{student_id}", response_model=StudentResponse)
def get_student(
        student_id:int,
        db: Session = Depends(get_db)
):
    return get_student_service(db,student_id)

#恢复学生
@router.put("/student_restore/{student_id}")
def restore_student(
        student_id:int,
        db: Session = Depends(get_db)
):
    return restore_student_service(db,student_id)

#查询所有学生列表
@router.get("/all")
def get_all_students(
        db: Session = Depends(get_db)
):
    return get_all_students_service(db)

#查询多个学生信息
# @router.get("/",response_model=StudentListResponse)
# def get_students(
#         page:int = 1,
#         page_size:int = 10,
#         keyword:str = None,
#         class_id:int = None,
#         db: Session = Depends(get_db)
# ):
#     return get_student_service(db,page,page_size,keyword,class_id)


