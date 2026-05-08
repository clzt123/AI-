from sqlalchemy.orm import Session
from models.teacher import Teacher
from schemas.teacher import TeacherCreate, TeacherUpdate

# 新增老师
def create_teacher(db: Session, t: TeacherCreate):
    db_tea = Teacher(**t.model_dump())
    db.add(db_tea)
    db.commit()
    db.refresh(db_tea)
    return db_tea

# 更新老师
def update_teacher(db: Session, teacher_id: int, data: TeacherUpdate):
    tea = db.query(Teacher).filter(
        Teacher.teacher_id == teacher_id,
        Teacher.is_deleted == 0
    ).first()
    if not tea:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(tea, key, value)
    db.commit()
    db.refresh(tea)
    return tea

# 逻辑删除
def delete_teacher(db: Session, teacher_id: int):
    tea = db.query(Teacher).filter(
        Teacher.teacher_id == teacher_id
    ).first()
    if not tea:
        return False
    tea.is_deleted = 1
    db.commit()
    return True

#查询所有老师信息
def get_all_teachers(db: Session):
    teachers = db.query(Teacher)\
                 .filter(Teacher.is_deleted == 0)\
                 .all()
    return teachers

# 根据 ID 查询
def get_teacher_by_id(db: Session, teacher_id: int):
    return db.query(Teacher).filter(
        Teacher.teacher_id == teacher_id,
        Teacher.is_deleted == 0
    ).first()

# 条件查询 + 分页
def get_teacher_by_conditions(db: Session, teacher_name=None, gender=None, page=1, page_size=10):
    q = db.query(Teacher).filter(Teacher.is_deleted == 0)
    if teacher_name:
        q = q.filter(Teacher.teacher_name.like(f"%{teacher_name}%"))
    if gender:
        q = q.filter(Teacher.gender == gender)
    total = q.count()
    data = q.offset((page - 1) * page_size).limit(page_size).all()
    return total, data

#查询所有被删除的老师
def get_deleted_teachers(db: Session, page=1, page_size=10):
    q = db.query(Teacher).filter(Teacher.is_deleted == 1)
    total = q.count()
    data = q.offset((page - 1) * page_size).limit(page_size).all()
    return total, data

#恢复已删除老师
def restore_teacher(db: Session, teacher_id: int):
    tea = db.query(Teacher).filter(
        Teacher.teacher_id == teacher_id,
        Teacher.is_deleted == 1
    ).first()
    if not tea:
        return False
    tea.is_deleted = 0
    db.commit()
    db.refresh(tea)
    return tea

from sqlalchemy import func

# 统计男女老师人数
def get_teacher_stats(db: Session):
    result = db.query(
        Teacher.gender,
        func.count(Teacher.teacher_id)
    ).filter(
        Teacher.is_deleted == 0
    ).group_by(
        Teacher.gender
    ).all()

    stats = {"male_count": 0, "female_count": 0, "total": 0}
    for gender, count in result:
        stats['total'] += count
        if gender == '男':
            stats['male_count'] = count
        elif gender == '女':
            stats['female_count'] = count
    return stats

def check_teacher_exists(db: Session, teacher_id: int):
    return db.query(Teacher).filter(
        Teacher.teacher_id == teacher_id,
        Teacher.is_deleted == 0
    ).first() is not None

def check_teacher_deleted(db: Session, teacher_id: int):
    return db.query(Teacher).filter(
        Teacher.teacher_id == teacher_id,
        Teacher.is_deleted == 1
    ).first() is not None

def check_teacher_exists_any(db: Session, teacher_id: int):
    return db.query(Teacher).filter(
        Teacher.teacher_id == teacher_id
    ).first() is not None
