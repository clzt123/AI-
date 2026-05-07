from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dao.student_dao import *
from schemas.student_schemas import *
from models.student_model import StudentModel


#增加新学生信息
def create_student_service(db: Session,data:StudentCreate):
    if get_students_by_no(db,data.student_no):
        raise HTTPException(status_code=400,detail="学生编号已存在")
    db_student = create_student(db,data)
    return StudentResponse.model_validate(db_student)

#删除学生
def delete_student_service(db: Session,student_id:int):
    if not get_student_by_id(db,student_id):
        raise HTTPException(status_code=404,detail="学生不存在")
    delete_student(db,student_id)
    return {"message":"删除成功"}

#恢复学生
def restore_student_service(db: Session,student_id:int):
    db_student = db.query(StudentModel).filter(
        StudentModel.id == student_id,
        StudentModel.is_deleted == 1
    ).first()
    if not db_student:
        raise HTTPException(status_code=404,detail="学生不存在或未被删除")
    restore_student(db,student_id)
    return {"message":"恢复成功"}

#修改学生信息
def update_student_service(db: Session,student_id:int,data:StudentUpdate):
    if not get_student_by_id(db,student_id):
        raise HTTPException(status_code=404,detail="学生不存在")
    # 检查学号是否冲突
    if data.student_no:
        existing = get_students_by_no(db,data.student_no)
        if existing and existing.id != student_id:
            raise HTTPException(status_code=400,detail="学号已被占用")
    return update_student(db,student_id,data)

#查询学生信息
def get_student_service(db: Session,student_id:int):
    student = get_student_by_id(db,student_id)
    if not student:
        raise HTTPException(status_code=404,detail="学生不存在")
    return StudentResponse.model_validate(student)

#查询所有学生列表
def get_all_students_service(db: Session):
    students = get_all_students(db)
    return [StudentResponse.model_validate(s) for s in students]

# 查询多个学生
# def get_students_service(
#         db: Session,
#         page:int,
#         page_size:int,
#         keyword:str=None,
#         class_id:int=None
# ):
#     skip = (page - 1) * page_size
#     items = get_student_list(db,skip,page_size,keyword,class_id)
#     total = len(items)
#     return StudentListResponse(total=total,items=items)








