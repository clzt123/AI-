
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from dao.class_info_dao import get_all_classinfo, get_one_classinfo, put_update_classinfo, post_add_class, delete_class, \
    restore_class, count_class_month, get_class_by_lecturer_id, check_class_exists, check_class_name_exists


#所有班级信息：
def get_all_classinfo_service(db:Session):
    # 1. 调用dao层查询数据
    all_cls_service = get_all_classinfo(db)
    if not all_cls_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="暂无班级数据")
    return all_cls_service

#查询单个班级学生信息：
def get_one_classinfo_service(db:Session,class_id:int):
    one_cls_service = get_one_classinfo(db,class_id)
    if not one_cls_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="暂无班级数据")
    return one_cls_service

#添加班级：
def post_add_class_service(db: Session, cls_data):
    if not cls_data.class_name:
        raise HTTPException(status_code=400, detail="班级名称不能为空")

    if check_class_name_exists(db, cls_data.class_name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="班级名称已存在，不能重复添加" )

    return post_add_class(cls_data, db)

# 修改班级:
def put_update_class_service(db: Session, class_id: int, update_data):
    if not check_class_exists(db, class_id):
        raise HTTPException(status_code=404, detail="班级不存在")
    return put_update_classinfo(class_id, update_data, db)

#逻辑删除：
def delete_class_service(db: Session, class_id: int):
    if not check_class_exists(db, class_id):
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="班级不存在，无法删除")

    delete_class(class_id, db)

#恢复逻辑删除数据：
def restore_class_service(db: Session, class_id: int):
    if not check_class_exists(db, class_id, include_deleted=True):
        raise HTTPException(status_code=404, detail="班级不存在")

    if check_class_exists(db, class_id):
        raise HTTPException(status_code=400, detail="该班级未被删除，无需恢复")
    restore_class(class_id, db)

# 按月统计班级数 service
def count_class_month_service(db: Session, month: str = None):
    data = count_class_month(db, month=month)  # 把 month 传给 DAO
    if not data:
        raise HTTPException(status_code=404, detail="暂无数据")
    return data

#按上课老师id查他的上课班级名：
def get_class_by_lecturer_id_service(db: Session,lecturer_id: int):
    if not get_class_by_lecturer_id(db, lecturer_id):
        raise HTTPException(status_code=404, detail="暂无班级数据")
    return get_class_by_lecturer_id(db,lecturer_id)