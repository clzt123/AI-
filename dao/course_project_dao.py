from sqlalchemy.orm import Session
from model.models import CourseProject

def get_course_by_filter(db: Session, target_education: str = None, target_country: str = None, target_major: str = None):
    query = db.query(CourseProject)
    if target_education:
        query = query.filter(CourseProject.target_education.like(f"%{target_education}%"))
    if target_country:
        query = query.filter(CourseProject.target_country.like(f"%{target_country}%"))
    if target_major:
        query = query.filter(CourseProject.target_major.like(f"%{target_major}%"))
    return query.all()
