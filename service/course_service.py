from sqlalchemy.orm import Session
from dao import course_project_dao
from model.schemas import CourseProjectResponse

def recommend_courses(db: Session, target_education: str = None, target_country: str = None, target_major: str = None):
    courses = course_project_dao.get_course_by_filter(db, target_education, target_country, target_major)
    return [CourseProjectResponse.model_validate(course) for course in courses]