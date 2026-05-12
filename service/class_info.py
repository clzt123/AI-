from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from dao.class_info import get_all_classes, get_one_class, create_class, update_class, delete_class, \
    restore_class, count_class_month, get_class_by_lecturer_id, check_class_exists, check_class_name_exists


def get_all_classinfo_service(db:Session) -> List:
    """获取所有班级信息列表"""
    all_classes = get_all_classes(db)
    return all_classes if all_classes else []

def get_one_classinfo_service(db:Session,class_id:int):
    """根据班级ID查询单个班级信息，不存在则抛出404异常"""
    class_info = get_one_class(db,class_id)
    if not class_info:
        raise HTTPException(status_code=404,detail="班级不存在")
    return class_info

def create_class_service(db: Session, cls_data):
    """创建新的班级信息记录，检查名称是否为空和是否重复"""
    if not cls_data.class_name:
        raise HTTPException(status_code=400, detail="班级名称不能为空")

    if check_class_name_exists(db, cls_data.class_name):
        raise HTTPException(status_code=400,detail="班级名称已存在，不能重复添加" )

    return create_class(db, cls_data)

def update_class_service(db: Session, class_id: int, update_data):
    """更新指定班级的信息，不存在则抛出404异常"""
    if not check_class_exists(db, class_id):
        raise HTTPException(status_code=404, detail="班级不存在")
    return update_class(db, class_id, update_data)

def delete_class_service(db: Session, class_id: int) -> None:
    """逻辑删除指定班级信息，不存在则抛出404异常"""
    if not check_class_exists(db, class_id):
        raise HTTPException(status_code=404, detail="班级不存在，无法删除")

    delete_class(db, class_id)

def restore_class_service(db: Session, class_id: int) -> None:
    """恢复已删除的班级信息，检查状态并防止无效恢复"""
    if not check_class_exists(db, class_id, include_deleted=True):
        raise HTTPException(status_code=404, detail="班级不存在")

    if check_class_exists(db, class_id):
        raise HTTPException(status_code=400, detail="该班级未被删除，无需恢复")
    restore_class(db, class_id)

def count_class_month_service(db: Session, month: str = None) -> List[Dict[str, Any]]:
    """统计每月开班数量，支持按月份筛选"""
    data = count_class_month(db, month=month)
    return data if data else []

def get_class_by_lecturer_id_service(db: Session,lecturer_id: int) -> List[str]:
    """根据讲师ID查询其负责的班级列表，无数据则抛出404异常"""
    if not get_class_by_lecturer_id(db, lecturer_id):
        raise HTTPException(status_code=404, detail="暂无班级数据")
    return get_class_by_lecturer_id(db,lecturer_id)
