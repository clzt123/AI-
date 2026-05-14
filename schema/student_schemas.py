from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class StudentAdminServiceCreate(BaseModel):
    student_id: Optional[int] = None
    service_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    approver_id: Optional[int] = None
    related_academic_id: Optional[int] = None


class StudentAdminServiceUpdate(BaseModel):
    student_id: Optional[int] = None
    service_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    approver_id: Optional[int] = None
    related_academic_id: Optional[int] = None


class StudentAdminServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    student_id: int
    service_type: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    reason: Optional[str]
    status: str
    approver_id: Optional[int]
    related_academic_id: Optional[int]
    create_time: datetime
    update_time: datetime


class StudentPsychProfileCreate(BaseModel):
    student_id: Optional[int] = None
    latest_emotion_tag: Optional[str] = None
    emotion_score: Optional[int] = None
    last_interaction_time: Optional[datetime] = None
    emotion_history: Optional[str] = None


class StudentPsychProfileUpdate(BaseModel):
    student_id: Optional[int] = None
    latest_emotion_tag: Optional[str] = None
    emotion_score: Optional[int] = None
    last_interaction_time: Optional[datetime] = None
    emotion_history: Optional[str] = None


class StudentPsychProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    student_id: int
    latest_emotion_tag: Optional[str]
    emotion_score: Optional[int]
    last_interaction_time: Optional[datetime]
    emotion_history: Optional[str]
    update_time: datetime


class StudentPsychAlertCreate(BaseModel):
    student_id: Optional[int] = None
    trigger_reason: Optional[str] = None
    risk_level: Optional[str] = None
    status: Optional[str] = None
    teacher_id: Optional[int] = None


class StudentPsychAlertUpdate(BaseModel):
    student_id: Optional[int] = None
    trigger_reason: Optional[str] = None
    risk_level: Optional[str] = None
    status: Optional[str] = None
    teacher_id: Optional[int] = None


class StudentPsychAlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    student_id: int
    trigger_reason: str
    risk_level: str
    status: str
    teacher_id: Optional[int]
    create_time: datetime


class StudentFeedbackTicketCreate(BaseModel):
    student_id: Optional[int] = None
    content: Optional[str] = None
    detail: Optional[str] = None
    status: Optional[str] = None
    solution: Optional[str] = None
    is_notified: Optional[int] = None


class StudentFeedbackTicketUpdate(BaseModel):
    student_id: Optional[int] = None
    content: Optional[str] = None
    detail: Optional[str] = None
    status: Optional[str] = None
    solution: Optional[str] = None
    is_notified: Optional[int] = None


class StudentFeedbackTicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    student_id: int
    content: str
    detail: Optional[str]
    status: str
    solution: Optional[str]
    is_notified: int
    create_time: datetime
    update_time: datetime


class StudyAbroadProgressCreate(BaseModel):
    student_id: Optional[int] = None
    service_stage: Optional[str] = None
    current_status: Optional[str] = None
    detail_info: Optional[str] = None
    last_update_time: Optional[datetime] = None
    update_by: Optional[int] = None


class StudyAbroadProgressUpdate(BaseModel):
    student_id: Optional[int] = None
    service_stage: Optional[str] = None
    current_status: Optional[str] = None
    detail_info: Optional[str] = None
    last_update_time: Optional[datetime] = None
    update_by: Optional[int] = None


class StudyAbroadProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    student_id: int
    service_stage: str
    current_status: str
    detail_info: Optional[str]
    last_update_time: datetime
    update_by: Optional[int]


class RawSQLRequest(BaseModel):
    sql: str