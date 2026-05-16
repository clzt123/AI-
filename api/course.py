from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from core.database import get_db
from service import course_service
from model.schemas import CourseProjectResponse
from typing import List, Optional

router = APIRouter()

@router.get("/recommend", response_model=List[CourseProjectResponse], summary="智能推荐课程项目")
def recommend_courses(
    target_education: Optional[str] = Query(None, description="适合学历"),
    target_country: Optional[str] = Query(None, description="目标国家"),
    target_major: Optional[str] = Query(None, description="意向专业"),
    db: Session = Depends(get_db)
):
    return course_service.recommend_courses(db, target_education, target_country, target_major)