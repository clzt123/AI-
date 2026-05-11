import re

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class EmploymentCreate(BaseModel):
    student_no: str = Field(pattern=r"^XS\d{7}$",description="学号")
    student_name: Optional[str] = Field(None)
    class_id: Optional[int] = Field(None)
    job_open_time: Optional[date] = Field(None,description="就业开始时间")
    offer_send_time: Optional[date] = Field(None,description="offer下发时间")
    company_name: Optional[str] = Field(None,description="公司名称")
    salary: Optional[int] = Field(None,description="薪资")


class EmploymentUpdate(BaseModel):
    student_name: Optional[str] = Field(None, description="学生姓名")
    class_id: Optional[int] = Field(None, description="班级id")
    job_open_time: Optional[date] = Field(None, description="就业开始时间")
    offer_send_time: Optional[date] = Field(None, description="offer下发时间")
    company_name: Optional[str] = Field(None, description="公司名称")
    salary: Optional[int] = Field(None, description="薪资")


class EmploymentResponse(BaseModel):
    employment_id: int
    student_no: str
    student_name: Optional[str]
    class_id: Optional[int]
    job_open_time: Optional[date] = None
    offer_send_time: Optional[date] = None
    company_name: Optional[str] = None
    salary: Optional[int] = None

    #数据库 ORM 对象实现自动序列化返回前端
    class Config:
        from_attributes = True