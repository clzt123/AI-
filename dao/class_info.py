from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional, Dict, Any
from models.class_info import ClassInfo
from schemas.class_info import ClassResponse, ClassUpdate


def get_all_classes(db:Session) -> List[ClassInfo]:
    """查询所有未删除的班级信息"""
    all_cls = db.query(ClassInfo).filter(ClassInfo.is_deleted == 0).all()
    return all_cls

def get_one_class(db: Session,class_id: int) -> Optional[ClassInfo]:
    """根据班级ID查询单个班级信息"""
    one_cls = db.query(ClassInfo).filter(ClassInfo.class_id == class_id, ClassInfo.is_deleted == 0).first()
    return one_cls

def create_class(db: Session, cls_data: ClassUpdate) -> ClassInfo:
    """创建新的班级信息记录"""
    try:
        new_class = ClassInfo(**cls_data.model_dump())
        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        return new_class
    except SQLAlchemyError:
        db.rollback()
        raise

def update_class(db: Session, class_id: int, update_data: ClassUpdate) -> ClassInfo:
    """更新指定班级的信息"""
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

def delete_class(db: Session, class_id: int) -> Optional[ClassInfo]:
    """逻辑删除指定班级信息"""
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

def restore_class(db: Session, class_id: int) -> Optional[ClassInfo]:
    """恢复已删除的班级信息"""
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

def check_class_exists(db: Session, class_id: int, include_deleted=False) -> bool:
    """检查班级是否存在，可选择是否包含已删除的"""
    q = db.query(ClassInfo).filter(ClassInfo.class_id == class_id)
    if not include_deleted:
        q = q.filter(ClassInfo.is_deleted == 0)
    return q.first() is not None

def check_class_name_exists(db: Session, class_name: str) -> bool:
    """检查班级名称是否已存在"""
    return db.query(ClassInfo).filter(
        ClassInfo.class_name == class_name,
        ClassInfo.is_deleted == 0
    ).first() is not None

def count_class_month(db: Session, month: str = None) -> List[Dict[str, Any]]:
    """统计每月开班数量，支持按月份筛选"""
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

def get_class_by_lecturer_id(db: Session,lecturer_id: int) -> List[str]:
    """根据讲师ID查询其负责的班级名称列表"""
    result = db.query(ClassInfo.class_name).filter(ClassInfo.lecturer_id == lecturer_id, ClassInfo.is_deleted == 0).all()
    return [row.class_name for row in result]

