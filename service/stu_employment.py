
from fastapi import HTTPException
from sqlalchemy.orm import Session
from dao.stu_employment import *
from schemas.stu_employment import EmploymentCreate

class EmploymentService:

    # 0. 获取所有就业信息
    def get_all(self, db: Session):
        return get_all_employment(db)

    # 1.新增就业信息（带学号重复校验）
    def create(self, data: EmploymentCreate, db: Session):
        # 查询学号是否已存在
        existing = get_emp_by_student_no(db, data.student_no)
        if existing:
            raise HTTPException(status_code=400, detail=f"学生编号 {data.student_no} 已存在")  # 已存在则抛400异常
        return create_employment(db, data)

    # 2. 根据学号查询（带判断）
    def get_by_student_no(self, student_no: str, db: Session):
        res = get_emp_by_student_no(db, student_no)
        if not res:
            raise HTTPException(status_code=404, detail="未找到该学生就业信息")
        return res

    # 3. 根据班级查询
    def get_by_class_id(self, class_id: int, db: Session):
        res = get_emp_by_class_id(db, class_id)
        if not res:
            raise HTTPException(status_code=404, detail=f"班级 {class_id} 暂无数据")
        return res

    # 4. 根据公司查询
    def get_by_company(self, company_name: str, db: Session):
        res = get_emp_by_company(db, company_name)
        if not res:
            raise HTTPException(status_code=404, detail=f"未找到 {company_name} 相关数据")
        return res

    # 5.根据薪资区间查寻
    def get_by_salary(self, min_salary: int, max_salary: int, db: Session):
        res = get_emp_by_salary(db, min_salary, max_salary)
        if not res:
            raise HTTPException(status_code=404, detail=f"无 {min_salary}~{max_salary} 薪资数据")
        return res
    # 6. 更新（带判断）
    def update(self, student_no: str, data: EmploymentCreate, db: Session):
        res = update_employment(db, student_no, data)
        if not res:
            raise HTTPException(status_code=404, detail="未找到，无法更新")
        return {"msg": "更新成功"}

    # 7. 删除（带判断）
    def delete(self, student_no: str, db: Session):
        if not delete_employment(db, student_no):
            raise HTTPException(status_code=404, detail="未找到，无法删除")
        return {"msg": "删除成功"}

    # 恢复已逻辑删除的就业信息
    def recover(self, student_no: str, db: Session):
            flag = recover_employment(db, student_no)
            if not flag:  ## 如果恢复失败（数据不存在或未被删除）
                raise HTTPException(
                    status_code=404,
                    detail="未找到已删除的学生数据"
                )
            return {"msg": "恢复成功"}