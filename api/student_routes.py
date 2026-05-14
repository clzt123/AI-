from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from service.student_service import BaseService
from schema.student_schemas import RawSQLRequest
from utils.sql_validator import validate_sql
from typing import Dict, Any, Optional

router = APIRouter()


@router.post("/{table_name}/create")
def create_record(
    table_name: str,
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    service = BaseService(db)
    result = service.create(table_name, data)
    if result is None:
        raise HTTPException(status_code=400, detail=f"表 {table_name} 不存在")
    return {"status": "success", "data": result}


@router.put("/{table_name}/update")
def update_record(
    table_name: str,
    data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    student_id = data.get("student_id")
    if student_id is None:
        raise HTTPException(status_code=400, detail="必须提供 student_id")
    
    service = BaseService(db)
    result = service.update_by_student_id(table_name, student_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"status": "success", "data": result}


@router.delete("/{table_name}/{id}")
def delete_record(
    table_name: str,
    id: int,
    db: Session = Depends(get_db)
):
    service = BaseService(db)
    success = service.delete(table_name, id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"status": "success", "message": "删除成功"}


@router.get("/{table_name}/{id}")
def get_record(
    table_name: str,
    id: int,
    db: Session = Depends(get_db)
):
    service = BaseService(db)
    result = service.get_by_id(table_name, id)
    if result is None:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"status": "success", "data": result}


@router.post("/query")
def execute_sql(
    request: RawSQLRequest,
    db: Session = Depends(get_db)
):
    sql = request.sql
    
    valid, error = validate_sql(sql)
    if not valid:
        raise HTTPException(status_code=400, detail=error)
    
    try:
        service = BaseService(db)
        result = service.execute_raw_sql(sql)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL 执行错误: {str(e)}")