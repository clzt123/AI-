from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.class_info_schemas import ClassResponse, ClassCreate, ClassUpdate
from service.class_info_service import get_all_classinfo_service, get_one_classinfo_service, post_add_class_service, \
    put_update_class_service, delete_class_service, restore_class_service, count_class_month_service, \
    get_class_by_lecturer_id_service

class_router = APIRouter(prefix="/class",tags=["班级管理"])

@class_router.get("/all")
def get_all_classinfo(db:Session = Depends(get_db)):
    res = get_all_classinfo_service(db)
    return {"code": 200, "message": "查询成功", "data": res}

@class_router.get("/one/{class_id}")
def get_one_classinfo(class_id: int,db: Session = Depends(get_db)):
    res = get_one_classinfo_service(db,class_id)
    return {"code": 200, "message": "查询成功", "data": res}

@class_router.post("/add")
def add_class(cls: ClassUpdate,db: Session = Depends(get_db)):
    return {"code": 200, "message": "添加成功", "data": post_add_class_service(db, cls)}

@class_router.put("/update/{class_id}")
def put_update_class(class_id: int,update_data: ClassUpdate,db: Session = Depends(get_db)):
    return {"code": 200, "message": "修改成功", "data": put_update_class_service(db, class_id, update_data)}

@class_router.delete("/delete/{class_id}", summary="删除班级")
def delete_class(class_id: int,db: Session = Depends(get_db)):
    delete_class_service(db, class_id)
    return {"code": 200, "message": "删除成功", "data": None}

@class_router.put("/restore/{class_id}", summary="恢复逻辑删除的班级")
def restore_class(class_id: int,db: Session = Depends(get_db)):
    restore_class_service(db, class_id)
    return {"code": 200, "message": "恢复成功", "data": None}

@class_router.get("/count/month")
def count_class_month(month: str = None, db: Session = Depends(get_db)):
    return {"code": 200, "message": "查询成功", "data": count_class_month_service(db, month=month)}

@class_router.get("/class_by_lecturer_id/{lecturer_id}")
def get_class_by_lecturer_id(lecturer_id: int,db: Session = Depends(get_db)):
    return {"code": 200, "message": "查询成功", "data": get_class_by_lecturer_id_service(db,lecturer_id)}
