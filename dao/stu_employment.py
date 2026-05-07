from sqlalchemy.orm import Session
from models.stu_employment import Employment
from schemas.stu_employment import *

# 获取所有就业信息
def get_all_employment(db: Session):
    return db.query(Employment).filter(
        Employment.is_deleted == 0
    ).all()

# 创建就业信息
def create_employment(db: Session, data: EmploymentCreate):
    emp = Employment(**data.dict())
    db.add(emp)
    db.commit()
    db.refresh(emp)
    return emp

def get_emp_by_student_no(db: Session, student_no: str):
    return db.query(Employment).filter(
        Employment.student_no == student_no,
        Employment.is_deleted == 0
    ).first()

# 根据班级ID查询
def get_emp_by_class_id(db: Session, class_id: int):
    return db.query(Employment).filter(
Employment.class_id == class_id,
        Employment.is_deleted == 0
    ).all()

# 根据公司模糊查询
def get_emp_by_company(db: Session, company_name: str):
    return db.query(Employment).filter(
        Employment.company_name.like(f"%{company_name}%"),
        Employment.is_deleted == 0
    ).all()

# 根据薪资范围查询
def get_emp_by_salary(db: Session, min_salary: int, max_salary: int):
    return db.query(Employment).filter(
        Employment.salary.between(min_salary, max_salary),
        Employment.is_deleted == 0
    ).all()

# 更新就业信息
def update_employment(db: Session, student_no: str, data: EmploymentCreate):
    emp = get_emp_by_student_no(db, student_no)
    if not emp:
        return None

    for key, value in data.dict().items():
        setattr(emp, key, value)

    db.commit()
    db.refresh(emp)
    return emp

# 逻辑删除
def delete_employment(db: Session, student_no: str):
    emp = get_emp_by_student_no(db, student_no)
    if not emp:
        return False

    emp.is_deleted = 1
    db.commit()
    return True

#恢复被逻辑删除的学生就业信息
def recover_employment(db: Session, student_no: str) :
    emp = db.query(Employment).filter(
        Employment.student_no == student_no,
        Employment.is_deleted == 1  # 只查已删除的数据
    ).first()

    if not emp:
        return False  # 数据不存在/未被删除，恢复失败

    emp.is_deleted = 0  # 恢复：把删除状态改回 0
    db.commit()
    return True