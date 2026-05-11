from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.class_info import ClassInfo
from schemas.class_info import ClassResponse, ClassUpdate


def get_all_classes(db:Session):
    all_cls = db.query(ClassInfo).filter(ClassInfo.is_deleted == 0).all()
    return all_cls

def get_one_class(db: Session,class_id: int):
    one_cls = db.query(ClassInfo).filter(ClassInfo.class_id == class_id, ClassInfo.is_deleted == 0).first()
    return one_cls

def create_class(db: Session, cls_data: ClassUpdate):
    try:
        new_class = ClassInfo(**cls_data.model_dump())
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        return new_class
    except SQLAlchemyError:
        db.rollback()
        raise

def update_class(db: Session, class_id: int, update_data):
    try:
        class_obj = db.query(ClassInfo).filter(ClassInfo.class_id == class_id, ClassInfo.is_deleted == 0).first()
        for k, v in update_data.model_dump(exclude_unset=True).items():
            setattr(class_obj, k, v)
        db.commit()
        db.refresh(class_obj)
        return class_obj
    except SQLAlchemyError:
        db.rollback()
        raise

def delete_class(db: Session, class_id: int):
    try:
        class_obj = db.query(ClassInfo).filter(ClassInfo.class_id == class_id).first()
        if not class_obj:
            return None
        class_obj.is_deleted = 1
        db.commit()
        return class_obj
    except SQLAlchemyError:
        db.rollback()
        raise

def restore_class(db: Session, class_id: int):
    try:
        class_obj = db.query(ClassInfo).filter(ClassInfo.class_id == class_id).first()
        if not class_obj:
            return None
        class_obj.is_deleted = 0
        db.commit()
        return class_obj
    except SQLAlchemyError:
        db.rollback()
        raise

def check_class_exists(db: Session, class_id: int, include_deleted=False):
    q = db.query(ClassInfo).filter(ClassInfo.class_id == class_id)
    if not include_deleted:
        q = q.filter(ClassInfo.is_deleted == 0)
    return q.first() is not None

def check_class_name_exists(db: Session, class_name: str):
    return db.query(ClassInfo).filter(
        ClassInfo.class_name == class_name,
        ClassInfo.is_deleted == 0
    ).first() is not None

def count_class_month(db: Session, month: str = None):
    query = db.query(
        func.DATE_FORMAT(ClassInfo.start_time, "%Y-%m").label("month"),
        func.count(ClassInfo.class_id).label("count"),
        func.group_concat(ClassInfo.class_name).label("class_names")
    ).filter(ClassInfo.is_deleted == 0)

    if month:
        query = query.filter(func.DATE_FORMAT(ClassInfo.start_time, "%Y-%m") == month.strip('"').strip("'"))

    result = query.group_by(
        func.DATE_FORMAT(ClassInfo.start_time, "%Y-%m")
    ).order_by("month").all()

    return [{ "month": row.month,
            "count": row.count,
            "class_names": row.class_names.split(",") } for row in result]

def get_class_by_lecturer_id(db: Session,lecturer_id: int):
    result = db.query(ClassInfo.class_name).filter(ClassInfo.lecturer_id == lecturer_id, ClassInfo.is_deleted == 0).all()
    return [row.class_name for row in result]

