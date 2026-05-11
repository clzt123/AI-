# 班级表模型
from sqlalchemy import Column, Integer, String, Date, SmallInteger, DateTime, func
from sqlalchemy.orm import relationship

from database import Base


class ClassInfo(Base):
    __tablename__ = "class_info"

    class_id = Column(Integer, primary_key=True, autoincrement=True,comment="班级编号")
    class_name = Column(String(50), nullable=False, comment="班级名称")
    start_time = Column(Date, nullable=True, comment="开课时间")
    head_teacher_id = Column(Integer, nullable=True, comment="班主任ID")
    lecturer_id = Column(Integer, nullable=True, comment="授课老师ID")
    is_deleted = Column(SmallInteger, nullable=False, default=0, comment="逻辑删除")
    create_time = Column(DateTime, default=func.now(), comment="创建时间")
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")

    # # 表建立 "一对多" 关联，让你可以跨表直接拿数据
    # students = relationship("Student", backref="class_info")