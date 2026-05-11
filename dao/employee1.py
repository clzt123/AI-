from sqlalchemy.orm import Session
from sqlalchemy import func
from models.employee1 import Employment
from schemas.employee1 import EmploymentCreate, EmploymentUpdate


class EmploymentDao:

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

    def get_by_salary_range(db: Session, salary_min: int, salary_max: int):
        return db.query(Employment).filter(
            Employment.salary.between(salary_min, salary_max),
            Employment.is_deleted == 0
        ).all()

    def get_salary_top5(db:Session):
        return db.query(Employment).filter(
            Employment.is_deleted == 0,
            Employment.salary.isnot(None)
        ).order_by(Employment.salary.desc()).limit(5).all()

    def get_class_avg(db:Session):
        return db.query(Employment.class_id,
                        func.avg(Employment.salary).label("avg_salary")
                        ).filter(
            Employment.is_deleted == 0,
            Employment.salary.isnot(None)
        ).group_by(Employment.class_id).all()

    def get_student_no_by(db:Session,student_no:str):
        return db.query(Employment).filter(Employment.student_no == student_no,
                                           Employment.is_deleted == 0).first()

    def get_employment_id_by(db:Session,employment_id:int):
        return db.query(Employment).filter(Employment.employment_id == employment_id,
                                           Employment.is_deleted == 0).first()

    def create_employment(db:Session,data:EmploymentCreate):
        emp = Employment(**data.model_dump())
        db.add(emp)
        db.commit()
        db.refresh(emp)
        return emp

    def update_employment(db:Session,employment_id:int,data:EmploymentUpdate):
        db.query(Employment).filter(Employment.employment_id == employment_id,
                                    Employment.is_deleted == 0).update(data.model_dump(exclude_unset=True))
        db.commit()

    def delete_employment(db:Session,employment_id:int):
        db.query(Employment).filter(
            Employment.employment_id == employment_id
        ).update({"is_deleted":1})
        db.commit()
        return employment_id

    def restore_employment(db:Session,employment_id:int):
        emp = db.query(Employment).filter(Employment.employment_id == employment_id).first()
        if not emp:
            return None
        emp.is_deleted = 0
        db.commit()
        db.refresh(emp)
        return emp




