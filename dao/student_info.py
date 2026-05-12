from sqlalchemy.orm import Session
from sqlalchemy import func, case
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Tuple
from models.student_info import Student
from schemas.student_info import StudentCreate, StudentUpdate

def create_student(db: Session, s: StudentCreate) -> Student:
    """
    创建新的学生信息记录
    
    参数:
        db: 数据库会话
        s: 学生创建数据
    
    返回:
        创建成功的学生对象
    
    异常:
        IntegrityError: 当违反数据库唯一约束时抛出
    """
    try:
        db_stu = Student(** s.model_dump())
        db.add(db_stu)
        db.commit()
        db.refresh(db_stu)
        return db_stu
    except IntegrityError:
        db.rollback()
        raise

def get_student(db: Session, id: int) -> Optional[Student]:
    """根据ID查询学生信息"""
    return db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first()

def get_students(db: Session, student_name=None, class_id=None, page=1, page_size=10) -> Tuple[int, List[Student]]:
    """根据条件查询学生信息并分页"""
    q = db.query(Student)
    q = q.filter(Student.is_deleted == 0)
    if student_name:
        q = q.filter(Student.student_name.contains(student_name))
    if class_id:
        q = q.filter(Student.class_id==class_id)
    total = q.count()
    data = q.offset((page-1)*page_size).limit(page_size).all()
    return total, data

def update_student(db: Session, id: int, data: StudentUpdate) -> Optional[Student]:
    """更新指定学生的信息"""
    try:
        stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first()
        if not stu:
            return None
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(stu, k, v)
        db.commit()
        db.refresh(stu) 
        return stu
    except IntegrityError:
        db.rollback()
        raise

def delete_student(db: Session, id: int) -> bool:
    """逻辑删除指定学生信息"""
    try:
        stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first()
        if not stu:
            return False
        stu.is_deleted = 1
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise

def restore_student(db: Session, id: int) -> bool:
    """恢复已删除的学生信息"""
    try:
        stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 1).first()
        if not stu:
            return False
        stu.is_deleted = 0
        db.commit()
        return True
    except IntegrityError:
        db.rollback()
        raise

def get_deleted_student(db: Session, student_name=None,page=1, page_size=10) -> Tuple[int, List[Student]]:
    """查询已删除的学生信息并分页"""
    q = db.query(Student).filter(Student.is_deleted == 1)
    if student_name:
        q = q.filter(Student.student_name.contains(student_name))
    total = q.count()
    data = q.offset((page-1)*page_size).limit(page_size).all()
    return total, data

def check_student_age(db: Session) -> List[Student]:
    """查询所有年龄超过30岁的学生信息"""
    stu_age = db.query(Student).filter(Student.is_deleted == 0,Student.age > 30).all()
    return stu_age

def check_student_gender(db: Session) -> List[dict]:
    """统计每个班级的总人数及男女生人数"""
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

