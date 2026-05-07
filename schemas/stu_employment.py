from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# 创建/更新 就业信息
class EmploymentCreate(BaseModel):
    student_no: str                # 学生编号
    student_name: str              # 学生姓名
    class_id: int                  # 班级ID
    job_open_time: Optional[datetime] = None    # 就业开放时间
    offer_send_time: Optional[datetime] = None  # offer时间
    company_name: Optional[str] = None          # 公司名
    salary: Optional[int] = None               # 薪资

# 响应给前端的格式
class EmploymentOut(EmploymentCreate):
    employment_id: int
    is_deleted: int


    class Config:
        from_attributes = True # 关键配置：允许直接把ORM数据库对象转为字典返回前端