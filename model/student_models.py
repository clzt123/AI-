from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from datetime import datetime
from core.database import Base


class StudentAdminService(Base):
    __tablename__ = "student_admin_service"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False, comment='学生ID')
    service_type = Column(String(100), nullable=False)
    start_time = Column(DateTime, comment='开始时间')
    end_time = Column(DateTime, comment='结束时间')
    reason = Column(String(100))
    status = Column(String(100), default='待审批')
    approver_id = Column(Integer)
    related_academic_id = Column(Integer)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class StudentPsychProfile(Base):
    __tablename__ = "student_psych_profile"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False, unique=True)
    latest_emotion_tag = Column(String(100))
    emotion_score = Column(Integer)
    last_interaction_time = Column(DateTime)
    emotion_history = Column(String(100))
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class StudentPsychAlert(Base):
    __tablename__ = "student_psych_alert"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    trigger_reason = Column(String(100), nullable=False)
    risk_level = Column(String(100), nullable=False)
    status = Column(String(100), default='未处理')
    teacher_id = Column(Integer)
    create_time = Column(DateTime, default=datetime.now)


class StudentFeedbackTicket(Base):
    __tablename__ = "student_feedback_ticket"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False)
    content = Column(String(100), nullable=False)
    detail = Column(String(100))
    status = Column(String(100), default='待处理')
    solution = Column(String(100))
    is_notified = Column(Integer, default=0)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class StudyAbroadProgress(Base):
    __tablename__ = "study_abroad_progress"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, nullable=False, comment='学生ID')
    service_stage = Column(String(50), nullable=False, comment='服务阶段（文书/申请/签证）')
    current_status = Column(String(100), nullable=False, comment='当前具体状态（如：初稿撰写中）')
    detail_info = Column(Text, comment='详细备注（如：文案老师正在润色PS第二段）')
    last_update_time = Column(DateTime, default=datetime.now, comment='最后更新时间')
    update_by = Column(Integer, comment='最后更新人（顾问ID）')


