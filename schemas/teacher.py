from pydantic import BaseModel,Field
from typing import Optional, List
from datetime import datetime,date
from enum import Enum


class GenderEnum(str, Enum):
    """性别枚举"""
    男 = "男"
    女 = "女"


class TeacherCreate(BaseModel):
    """新增老师请求体"""
    teacher_name: str=Field(...,max_length=10,min_length=2)
    gender: Optional[GenderEnum] = None
    phone: Optional[str] = None


class TeacherUpdate(BaseModel):
    """修改老师请求体"""
    teacher_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None


class TeacherResponse(BaseModel):
    """老师信息响应体"""
    teacher_id: int
    teacher_name: str
    gender: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True


class TeacherListResponse(BaseModel):
    """条件查询响应体"""
    total: int
    page: int
    page_size: int
    data: List[TeacherResponse]


class TeacherStatsResponse(BaseModel):
    """统计信息响应模型"""
    total: int
    male_count: int
    female_count: int

