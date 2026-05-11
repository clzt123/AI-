from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from models.employment import Employment
from schemas.employment import EmploymentCreate, EmploymentUpdate


class EmploymentDao:

    @staticmethod
    def get_all(
            db:Session,
            skip: int = 0,
            limit: int = 10,
            student_name: str = None,
            company_name:str = None,
            class_id: int = None
                ):
        emp = db.query(Employment).filter(Employment.is_deleted == 0)
        if student_name:
            emp = emp.filter(Employment.student_name.like(f"%{student_name}%"))
        if company_name:
            emp = emp.filter( Employment.company_name.like(f"%{company_name}%"))
        if class_id:
            emp = emp.filter(Employment.class_id == class_id)
        return emp.offset(skip).limit(limit).all()

    @staticmethod
    def get_by_salary_range(db: Session, salary_min: int, salary_max: int):
        return db.query(Employment).filter(
            Employment.salary.between(salary_min, salary_max),
            Employment.is_deleted == 0
        ).all()

    @staticmethod
    def get_salary_top5(db:Session):
        return db.query(Employment).filter(
            Employment.is_deleted == 0,
            Employment.salary.isnot(None)
        ).order_by(Employment.salary.desc()).limit(5).all()

    @staticmethod
    def get_class_avg(db:Session):
        return db.query(Employment.class_id,
                        func.avg(Employment.salary).label("avg_salary")
                        ).filter(
            Employment.is_deleted == 0,
            Employment.salary.isnot(None)
        ).group_by(Employment.class_id).all()

    @staticmethod
    def get_student_no_by(db:Session,student_no:str):
        return db.query(Employment).filter(Employment.student_no == student_no,
                                           Employment.is_deleted == 0).first()

    @staticmethod
    def get_employment_id_by(db:Session,employment_id:int):
        return db.query(Employment).filter(Employment.employment_id == employment_id,
                                           Employment.is_deleted == 0).first()

    @staticmethod
    def create_employment(db:Session,data:EmploymentCreate):
        try:
            emp = Employment(**data.model_dump())
            db.add(emp)
            db.commit()
            db.refresh(emp)
            return emp
        except SQLAlchemyError:
            db.rollback()
            raise

    @staticmethod
    def update_employment(db:Session,employment_id:int,data:EmploymentUpdate):
        try:
            db.query(Employment).filter(Employment.employment_id == employment_id,
                                        Employment.is_deleted == 0).update(data.model_dump(exclude_unset=True))
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise

    @staticmethod
    def delete_employment(db:Session,employment_id:int):
        try:
            db.query(Employment).filter(
                Employment.employment_id == employment_id
            ).update({"is_deleted":1})
            db.commit()
            return employment_id
        except SQLAlchemyError:
            db.rollback()
            raise

    @staticmethod
    def restore_employment(db:Session,employment_id:int):
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




