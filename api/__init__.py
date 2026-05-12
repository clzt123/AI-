"""
API 路由模块
包含所有 HTTP 接口定义，按业务模块拆分：
- student_info: 学生管理
- teacher: 老师管理
- score: 成绩管理
- class_info: 班级管理
- employment: 就业管理
"""
from .class_info import class_router
from .employment import router as employment_router
from .score import score_router
from .student_info import router as student_info_router
from .teacher import router as teacher_router
from .user import user_router
