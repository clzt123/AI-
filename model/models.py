from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from core.database import Base

class CourseProject(Base):
    __tablename__ = "course_project"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="项目ID")
    project_name = Column(String(100), nullable=False, comment="项目/课程名称")
    category = Column(String(50), comment="类别（如：语言培训、背景提升、硕博连读）")
    target_education = Column(String(50), comment="适合学历")
    duration = Column(String(50), comment="学制时长")
    tuition_fee = Column(String(50), comment="学费")
    project_advantage = Column(String(500), comment="项目优势")
    application_condition = Column(String(500), comment="申请条件")
    target_country = Column(String(50), comment="目标国家")
    target_major = Column(String(100), comment="意向专业")
    status = Column(String(20), default='招生中', comment="招生状态")

class EventLecture(Base):
    __tablename__ = "event_lecture"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    event_name = Column(String(100), nullable=False, comment="活动名称")
    event_type = Column(String(20), comment="活动类型（线上/线下）")
    start_time = Column(DateTime, comment="开始时间")
    location = Column(String(200), comment="地点/会议链接")
    max_participants = Column(Integer, comment="最大报名人数")
    current_participants = Column(Integer, default=0, comment="已报名人数")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

class EventRegistration(Base):
    __tablename__ = "event_registration"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键ID")
    event_id = Column(Integer, nullable=False, comment="活动ID")
    customer_name = Column(String(50), comment="客户姓名")
    phone = Column(String(20), comment="联系电话")
    email = Column(String(100), comment="邮箱")
    remark = Column(Text, comment="备注")
    status = Column(String(20), default="已报名", comment="报名状态")
    create_time = Column(DateTime, default=datetime.now, comment="报名时间")
