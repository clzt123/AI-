from sqlalchemy.orm import Session
from sqlalchemy import func, case
from sqlalchemy.exc import SQLAlchemyError
from models.student_info import Student
from schemas.student_info import StudentCreate, StudentUpdate

# 创建：数据库自动生成id
def create_student(db: Session, s: StudentCreate):
    try:
        db_stu = Student(** s.model_dump())
        db.add(db_stu)
        db.commit()
        db.refresh(db_stu)
        return db_stu
    except SQLAlchemyError:
        db.rollback()
        raise

# 查询按 id（主键）
def get_student(db: Session, id: int):
    return db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first()

# 条件查询
def get_students(db: Session, student_name=None, class_id=None, page=1, page_size=10):
    q = db.query(Student)
    q = q.filter(Student.is_deleted == 0)
    if student_name:
        q = q.filter(Student.student_name.contains(student_name))
    if class_id:
        q = q.filter(Student.class_id==class_id)
    total = q.count()
    data = q.offset((page-1)*page_size).limit(page_size).all()
    return total, data

# 更新按 id
def update_student(db: Session, id: int, data: StudentUpdate):
    try:
        stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first()
        if not stu:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(stu, k, v)
        db.commit()
        db.refresh(stu) 
        return stu
    except SQLAlchemyError:
        db.rollback()
        raise

# 删除按 id
def delete_student(db: Session, id: int):
    try:
        stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first()
        if not stu:
            return False
        stu.is_deleted = 1
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise

#恢复学生数据
def restore_student(db: Session, id: int):
    try:
        stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 1).first()
        if not stu:
            return False
        stu.is_deleted = 0
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise

#查询已删除学生的数据
# 删除按 id
def delete_student(db: Session, id: int):
    stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first()
    if not stu:
        return False
    stu.is_deleted = 1
    db.commit()
    return True

#恢复学生数据
def restore_student(db: Session, id: int):
    stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 1).first()
    if not stu:
        return False
    stu.is_deleted = 0
    db.commit()
    return True

#查询已删除学生的数据
def get_deleted_student(db: Session, student_name=None,page=1, page_size=10):
    q = db.query(Student).filter(Student.is_deleted == 1)
    if student_name:
        q = q.filter(Student.student_name.contains(student_name))
    total = q.count()
    data = q.offset((page-1)*page_size).limit(page_size).all()
    return total, data

# 查询所有超过30岁的学员信息
def check_student_age(db: Session):
    stu_age = db.query(Student).filter(Student.is_deleted == 0,Student.age > 30).all()
    return stu_age

#统计每个班级的人数以及男生女生人数
def check_student_gender(db: Session):
    stu = (db.query(
        Student.class_id.label("class_id"),
        func.count(Student.id).label('total_count'),
        func.sum(func.if_(Student.gender == "男", 1, 0)).label("male_count"),
        func.sum(func.if_(Student.gender == "女", 1, 0)).label("female_count")
    )
    .filter(Student.is_deleted == 0)
    .group_by(Student.class_id)
    .all())
    result = []
    for s in stu:
        result.append({
            "class_id": s.class_id,
            "total_count": s.total_count,
            "male_count": s.male_count if s.male_count is not None else 0,
            "female_count": s.female_count if s.female_count is not None else 0
        })
    return result

