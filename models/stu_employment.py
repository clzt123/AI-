
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

# 创建学生就业表结构
class Employment(Base):
    __tablename__ = "employment2"
    employment_id = Column(Integer, primary_key=True, autoincrement=True, comment="就业ID") # 就业ID 主键自增
    student_no = Column(String(50), nullable=False, unique=True, comment="学生编号")
    student_name = Column(String(50), nullable=False, comment="学生姓名")
    class_id = Column(Integer, nullable=False, index=True, comment="班级ID")
    job_open_time = Column(DateTime, nullable=True, comment="就业开放时间")
    offer_send_time = Column(DateTime, nullable=True, comment="offer下发时间")
    company_name = Column(String(100), index=True, comment="就业公司")
    salary = Column(Integer, index=True, comment="就业薪资")
    # 逻辑删除 0=未删除 1=已删除
    is_deleted = Column(Integer, default=0, nullable=False, comment="逻辑删除 0-未删 1-删除")

