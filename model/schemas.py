from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# 课程项目相关
class CourseProjectResponse(BaseModel):
    id: int
    project_name: str
    category: str
    target_education: str
    duration: str
    tuition_fee: str
    project_advantage: str
    application_condition: str
    target_country: str
    target_major: str
    status: str
    class Config:
        from_attributes = True

# 活动相关
class EventLectureResponse(BaseModel):
    id: int
    event_name: str
    event_type: str
    start_time: datetime
    location: str
    max_participants: int
    current_participants: int
    class Config:
        from_attributes = True

class EventRegistrationCreate(BaseModel):
    event_id: int
    customer_name: str
    phone: str
    email: Optional[EmailStr] = None
    remark: Optional[str] = None

class EventRegistrationResponse(BaseModel):
    id: int
    event_id: int
    customer_name: str
    phone: str
    email: Optional[str]
    status: str
    create_time: datetime
    class Config:
        from_attributes = True
