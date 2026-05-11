from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from models.employment import Employment
from schemas.employment import EmploymentCreate, EmploymentUpdate


def get_all_employment(
        db: Session,
        skip: int = 0,
        limit: int = 10,
        student_name: str = None,
        company_name: str = None,
        class_id: int = None
) -> List[Employment]:
    """查询所有未删除的就业信息，支持分页和多条件筛选"""
    emp = db.query(Employment).filter(Employment.is_deleted == 0)
    if student_name:
        emp = emp.filter(Employment.student_name.like(f"%{student_name}%"))
    if company_name:
        emp = emp.filter(Employment.company_name.like(f"%{company_name}%"))
    if class_id:
        emp = emp.filter(Employment.class_id == class_id)
    return emp.offset(skip).limit(limit).all()


def get_by_salary_range(db: Session, salary_min: int, salary_max: int) -> List[Employment]:
    """根据薪资范围查询就业信息"""
    return db.query(Employment).filter(
        Employment.salary.between(salary_min, salary_max),
        Employment.is_deleted == 0
    ).all()


def get_salary_top5(db: Session) -> List[Employment]:
    """查询薪资最高的5条就业信息"""
    return db.query(Employment).filter(
        Employment.is_deleted == 0,
        Employment.salary.isnot(None)
    ).order_by(Employment.salary.desc()).limit(5).all()


def get_class_avg(db: Session):
    """统计每个班级的平均薪资"""
    return db.query(Employment.class_id,
                    func.avg(Employment.salary).label("avg_salary")
                    ).filter(
        Employment.is_deleted == 0,
        Employment.salary.isnot(None)
    ).group_by(Employment.class_id).all()


def get_student_no_by(db: Session, student_no: str) -> Optional[Employment]:
    """根据学号查询就业信息"""
    return db.query(Employment).filter(Employment.student_no == student_no,
                                       Employment.is_deleted == 0).first()


def get_employment_id_by(db: Session, employment_id: int) -> Optional[Employment]:
    """根据就业ID查询就业信息"""
    return db.query(Employment).filter(Employment.employment_id == employment_id,
                                       Employment.is_deleted == 0).first()


def create_employment(db: Session, data: EmploymentCreate) -> Employment:
    """创建新的就业信息记录"""
    try:
        emp = Employment(**data.model_dump())
        db.add(emp)
        db.commit()
        db.refresh(emp)
        return emp
    except SQLAlchemyError:
        db.rollback()
        raise


def update_employment(db: Session, employment_id: int, data: EmploymentUpdate) -> None:
    """更新指定就业信息记录"""
    try:
        db.query(Employment).filter(Employment.employment_id == employment_id,
                                    Employment.is_deleted == 0).update(data.model_dump(exclude_unset=True))
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_employment(db: Session, employment_id: int) -> int:
    """逻辑删除指定就业信息记录"""
    try:
        db.query(Employment).filter(
            Employment.employment_id == employment_id
        ).update({"is_deleted": 1})
        db.commit()
        return employment_id
    except SQLAlchemyError:
        db.rollback()
        raise


def restore_employment(db: Session, employment_id: int) -> Optional[Employment]:
    """恢复已删除的就业信息记录"""
    try:
        emp = db.query(Employment).filter(Employment.employment_id == employment_id).first()
        if not emp:
            return None
        emp.is_deleted = 0
        db.commit()
        db.refresh(emp)
        return emp
    except SQLAlchemyError:
        db.rollback()
        raise
