from sqlalchemy.orm import Session
from models.student_model import StudentModel
from schemas.student_schemas import StudentCreate, StudentUpdate

#新增学生数据
def create_student(db:Session,student_data:StudentCreate):
    #把前端传来的Pydantic数据，转换成数据库能识别的ORM模型对象。
    db_student = StudentModel(**student_data.model_dump())
    db.add(db_student)
    db.commit()
    #强制从数据库重新查询一遍最新数据，覆盖当前模型对象的属性。
    db.refresh(db_student)
    return db_student

#逻辑删除
def delete_student(db:Session,student_id:int):
    db_student = get_student_by_id(db,student_id)
    if db_student:
        db_student.is_deleted = 1
        db.commit()
        db.refresh(db_student)
    return db_student

#恢复逻辑删除
def restore_student(db:Session,student_id:int):
    db_student = db.query(StudentModel).filter(
        StudentModel.id == student_id,
        StudentModel.is_deleted == 1
    ).first()
    if db_student:
        db_student.is_deleted = 0
        db.commit()
        db.refresh(db_student)
    return db_student

def check_student_exists(db:Session,student_id:int):
    return db.query(StudentModel).filter(
        StudentModel.id == student_id,
        StudentModel.is_deleted == 0
    ).first() is not None

def check_student_deleted(db:Session,student_id:int):
    return db.query(StudentModel).filter(
        StudentModel.id == student_id,
        StudentModel.is_deleted == 1
    ).first() is not None

def check_student_exists_any(db:Session,student_id:int):
    return db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first() is not None

#更新学生数据
def update_student(db:Session,student_id:int,student_data:StudentUpdate):
    db_student = get_student_by_id(db,student_id)
    if db_student:
        update_data = student_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

#根据id查询
def get_student_by_id(db:Session,student_id:int):
    return db.query(StudentModel).filter(
        StudentModel.id == student_id,
        StudentModel.is_deleted == 0
    ).first()

#根据学号查询
def get_students_by_no(db:Session,student_no:str):
    return db.query(StudentModel).filter(
        StudentModel.student_no == student_no,
        StudentModel.is_deleted == 0
    ).first()

#获取所有学生列表
def get_all_students(db:Session):
    return db.query(StudentModel).filter(
        StudentModel.is_deleted == 0
    ).all()

# 查询列表，关键字，班级id
# def get_student_list(
#         db: Session,
#         skip:int,
#         limit:int,
#         keyword:str=None,
#         class_id:int=None
# ):
#     query =db.query(StudentModel).filter(StudentModel.is_deleted==0)
#     if keyword:
#         query = query.filter(
#             (StudentModel.student_name.like(f"%{keyword}%"))|
#             (StudentModel.student_no.like(f"%{keyword}%"))
#         )
#     if class_id:
#         query = query.filter(StudentModel.class_id==class_id)
#     return query.offset(skip).limit(limit).all()
#









