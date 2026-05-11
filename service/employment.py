#业务逻辑处理层：处理业务，调用dao层
# 全部使用 @staticmethod 静态方法
from fastapi import HTTPException
from sqlalchemy.orm import Session
from dao.employment import EmploymentDao
from schemas.employment import EmploymentResponse, EmploymentCreate, EmploymentUpdate


class EmploymentService:
    #分页查询所有就业记录
    @staticmethod
    def get_all_service(db:Session,skip:int,limit:int,student_name: str,company_name:str,class_id: int):
        return EmploymentDao.get_all(db, skip, limit, student_name,company_name, class_id)

    # 按薪资区间查询
    @staticmethod
    def get_by_salary_range_service(db: Session, salary_min: int, salary_max: int):
        emp_list = EmploymentDao.get_by_salary_range(db, salary_min, salary_max)
        return emp_list

    #就业统计模块分析
    @staticmethod
    def get_statistics_service(db:Session):
        #薪资前五
        top5 = EmploymentDao.get_salary_top5(db)
        #班级平均薪资
        class_avg_salary = EmploymentDao.get_class_avg(db)
        # 把获取的class_avg_salary平均薪资遍历并添加到空列表中
        class_result = []
        for item in class_avg_salary:
            class_result.append({
                "class_id": item.class_id,
                "avg_salary": float(item.avg_salary) if item.avg_salary else 0
            })

        return {
            "salary_top5": [EmploymentResponse.model_validate(i).model_dump() for i in top5],
            "class_average_salary": class_result
        }

    # 通过学号查询就业记录
    @staticmethod
    def get_student_no_service(db:Session,student_no:str):
        emp = EmploymentDao.get_student_no_by(db,student_no)
        if not emp:
            raise HTTPException(status_code=404, detail="就业信息不存在")
        return emp

    # 通过就业id查询单条就业记录
    @staticmethod
    def get_employment_id_service(db:Session,employment_id:int):
        return EmploymentDao.get_employment_id_by(db,employment_id)

    #新增就业数据，通过service处理业务
    @staticmethod
    def create_employment_service(db:Session,data:EmploymentCreate):
        exist = EmploymentDao.get_student_no_by(db,data.student_no)
        if exist:
            raise HTTPException(status_code=409, detail="就业信息已存在")
        return EmploymentDao.create_employment(db,data)

    #修改前端传过来的就业数据,在service层做简单的业务处理
    @staticmethod
    def update_employment_service(db:Session,employment_id:int,data:EmploymentUpdate):
        emp = EmploymentDao.get_employment_id_by(db,employment_id)
        if not emp:
            raise HTTPException(status_code=404, detail="就业信息不存在")
        EmploymentDao.update_employment(db,employment_id,data)
        return EmploymentDao.get_employment_id_by(db,employment_id)

    #逻辑删除就业记录
    @staticmethod
    def delete_employment_service(db:Session,employment_id:int):
        emp = EmploymentDao.get_employment_id_by(db,employment_id)
        if not emp:
            raise HTTPException(status_code=404, detail="就业信息不存在")
        EmploymentDao.delete_employment(db, employment_id)
        return {"code": 200, "message": "删除成功", "data": employment_id}

 # 恢复逻辑删除的数据
    @staticmethod
    def restore_employment_service(db: Session, employment_id: int):
        #调用dao层
        emp = EmploymentDao.restore_employment(db,employment_id)
        #进行条件判断，如果数据不存在，则抛出异常
        if not emp:
            raise HTTPException(status_code=404,detail="就业信息不存在，无法恢复")
        return emp













