from sqlalchemy import Column, Integer, String, DateTime, func
from database import Base


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(50), unique=True, nullable=False, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    role = Column(String(20), nullable=False, comment="角色: admin-管理员, homeroom-班主任, teacher-任课老师")
    real_name = Column(String(50), nullable=True, comment="真实姓名")
    phone = Column(String(20), nullable=True, comment="联系电话")
    is_deleted = Column(Integer, nullable=False, default=0, comment="逻辑删除 0-未删 1-已删")
    create_time = Column(DateTime, default=func.now(), comment="创建时间")
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment="更新时间")
