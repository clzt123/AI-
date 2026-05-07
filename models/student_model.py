# 1. 从 SQLAlchemy 导入需要的字段类型
from sqlalchemy import Column, Integer, String, Date
# 2. 从自己项目的 database.py 导入 Base 基类
from database import Base

class StudentModel(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True,autoincrement=True,comment="学生编号")
    student_no = Column(String(50), unique=True,comment="学生业务号")
    class_id = Column(Integer,comment="班级id")
    student_name = Column(String(50),comment="学生姓名")
    gender = Column(String(10),comment="性别")
    age = Column(Integer,comment="年龄")
    native_place = Column(String(100),comment="籍贯")
    graduate_school = Column(String(100),comment="毕业院校")
    major = Column(String(100),comment="专业")
    education = Column(String(50),comment="学历")
    admission_time = Column(Date,comment="入学时间")
    graduate_time = Column(Date,comment="毕业时间")
    advisor_id = Column(Integer,comment="顾问编号")
    is_deleted = Column(Integer,nullable=False,default=0,comment='逻辑删除 0-未删 1-已删')#非空，默认值为0

