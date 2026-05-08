from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from service.stu_employment import EmploymentService
from schemas.stu_employment import EmploymentCreate, EmploymentOut

router = APIRouter(
    prefix="/employment2",
    tags=["学生就业管理"]
)

service = EmploymentService()

@router.get("/all")
def get_all(db: Session = Depends(get_db)):
    return service.get_all(db)

@router.post("/add", response_model=EmploymentOut)
def create(data: EmploymentCreate, db: Session = Depends(get_db)):
    return service.create(data, db)

@router.get("/check/{student_no}", response_model=EmploymentOut)
def get_by_no(student_no: str, db: Session = Depends(get_db)):
    return service.get_by_student_no(student_no, db)

@router.get("/class/{class_id}")
def get_by_class(class_id: int, db: Session = Depends(get_db)):
    return service.get_by_class_id(class_id, db)

@router.get("/company/{name}")
def get_by_company(name: str, db: Session = Depends(get_db)):
    return service.get_by_company(name, db)

@router.get("/salary/{min_salary}/{max_salary}")
def get_by_salary(min_salary: int, max_salary: int, db: Session = Depends(get_db)):
    return service.get_by_salary(min_salary, max_salary, db)

@router.put("/update/{student_no}")
def update(student_no: str, data: EmploymentCreate, db: Session = Depends(get_db)):
    return service.update(student_no, data, db)

@router.delete("/delete/{student_no}")
def delete(student_no: str, db: Session = Depends(get_db)):
    service.delete(student_no, db)
    return {"code": 200, "message": "删除成功", "data": None}

@router.post("/recover/{student_no}")
def recover(student_no: str, db: Session = Depends(get_db)):
    service.recover(student_no, db)
    return {"code": 200, "message": "恢复成功", "data": None}
