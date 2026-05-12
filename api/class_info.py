from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any, List

from database import get_db
from schemas.class_info import ClassResponse, ClassCreate, ClassUpdate
from service.class_info import get_all_classinfo_service, get_one_classinfo_service, create_class_service, \
    update_class_service, delete_class_service, restore_class_service, count_class_month_service, \
    get_class_by_lecturer_id_service
from service.auth import require_permission, AuthUser

router = APIRouter(prefix="/classes",tags=["班级管理"])

@router.get("/all", response_model=dict)
def get_all_classinfo(db:Session = Depends(get_db)) -> Dict[str, Any]:
    """获取所有班级信息列表"""
    res = get_all_classinfo_service(db)
    return {"code": 200, "message": "查询成功", "data": [ClassResponse.model_validate(item).model_dump() for item in res]}

@router.get("/one/{class_id}", response_model=dict)
def get_one_classinfo(class_id: int,db: Session = Depends(get_db)) -> Dict[str, Any]:
    """根据班级ID查询单个班级信息"""
    res = get_one_classinfo_service(db,class_id)
    return {"code": 200, "message": "查询成功", "data": ClassResponse.model_validate(res).model_dump()}

@router.post("/add", response_model=dict)
def create_class(cls_data: ClassCreate,db: Session = Depends(get_db), _: AuthUser = Depends(require_permission("class_info", "create"))) -> Dict[str, Any]:
    """创建新的班级信息记录"""
    return {"code": 200, "message": "添加成功", "data": ClassResponse.model_validate(create_class_service(db, cls_data)).model_dump()}

@router.put("/update/{class_id}", response_model=dict)
def update_class(class_id: int,update_data: ClassUpdate,db: Session = Depends(get_db), _: AuthUser = Depends(require_permission("class_info", "update"))) -> Dict[str, Any]:
    """更新指定班级的信息"""
    return {"code": 200, "message": "修改成功", "data": ClassResponse.model_validate(update_class_service(db, class_id, update_data)).model_dump()}

@router.delete("/delete/{class_id}", summary="删除班级", response_model=dict)
def delete_class(class_id: int,db: Session = Depends(get_db), _: AuthUser = Depends(require_permission("class_info", "delete"))) -> Dict[str, Any]:
    """逻辑删除指定班级信息"""
    delete_class_service(db, class_id)
    return {"code": 200, "message": "删除成功", "data": None}

@router.put("/restore/{class_id}", summary="恢复逻辑删除的班级", response_model=dict)
def restore_class(class_id: int,db: Session = Depends(get_db), _: AuthUser = Depends(require_permission("class_info", "restore"))) -> Dict[str, Any]:
    """恢复已删除的班级信息"""
    restore_class_service(db, class_id)
    return {"code": 200, "message": "恢复成功", "data": None}

@router.get("/count/month", response_model=dict)
def count_class_month(month: str = None, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """统计每月开班数量，支持按月份筛选"""
    return {"code": 200, "message": "查询成功", "data": count_class_month_service(db, month=month)}

@router.get("/class_by_lecturer_id/{lecturer_id}", response_model=dict)
def get_class_by_lecturer_id(lecturer_id: int,db: Session = Depends(get_db)) -> Dict[str, Any]:
    """根据讲师ID查询其负责的班级列表"""
    return {"code": 200, "message": "查询成功", "data": get_class_by_lecturer_id_service(db,lecturer_id)}
