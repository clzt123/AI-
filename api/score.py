from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from service.score import (
    add_score_service, get_scores_service, update_score_service,
    delete_score_service, restore_score_service,
    get_all_above_80_service, get_multiple_fail_service, get_class_avg_service
)
from schemas.score import (
    ScoreCreate, ScoreUpdate, ScoreResponse, ScoreResponseItem, Score_Page_Response,
    StudentFailResponse, ClassAvgScoreResponse
)
from database import get_db
from service.auth import require_permission, AuthUser

score_router = APIRouter()

@score_router.post('/scores', response_model=dict, summary="添加成绩")
def add_score(score: ScoreCreate, db: Session = Depends(get_db), _: AuthUser = Depends(require_permission("score", "create"))) -> Dict[str, Any]:
    """添加新的成绩记录"""
    result = add_score_service(db, score)
    return {"code": 200, "message": "添加成功", "data": ScoreResponseItem.model_validate(result).model_dump()}

@score_router.get('/scores', response_model=Score_Page_Response, summary="综合查询成绩")
def get_scores(
    id: int | None = Query(None, description="成绩ID", ge=1),
    student_no: str | None = Query(None, description="学生学号", min_length=1, max_length=20),
    exam_order: int | None = Query(None, description="考试序号", ge=1),
    page: int = Query(1, description="页码", ge=1),
    page_size: int = Query(10, description="每页条数", ge=1, le=50),
    db: Session = Depends(get_db)
) -> Score_Page_Response:
    """分页查询成绩信息，支持按学号、考试序号筛选"""
    result = get_scores_service(db, id, student_no, exam_order, page, page_size)
    return result

@score_router.put("/scores/{id}", summary="修改成绩")
def update_score(id: int, update_data: ScoreUpdate, db: Session = Depends(get_db), _: AuthUser = Depends(require_permission("score", "update"))) -> Dict[str, Any]:
    """更新指定成绩记录"""
    data = update_score_service(db, id, update_data)
    return {"code":200,"message":"修改成功","data": ScoreResponseItem.model_validate(data).model_dump() if data else None}

@score_router.delete("/scores/{id}", summary="删除成绩")
def delete_score(id: int, db: Session = Depends(get_db), _: AuthUser = Depends(require_permission("score", "delete"))) -> Dict[str, Any]:
    """逻辑删除指定成绩记录"""
    delete_score_service(db, id)
    return {"code":200,"message":"删除成功","data":None}

@score_router.put("/scores/delete/restore", summary="批量/单条恢复已删除成绩")
def restore_score(
    id: int = None,
    student_no: str = None,
    exam_order: int = None,
    db: Session = Depends(get_db),
    _: AuthUser = Depends(require_permission("score", "restore"))
) -> Dict[str, Any]:
    """恢复已删除的成绩记录，支持批量恢复"""
    count = restore_score_service(db, id, student_no, exam_order)
    return {"code": 200, "message": f"恢复成功，共恢复 {count} 条", "data": {"count": count}}

@score_router.get("/scores/all-above-80", summary="查询80分以上学生")
def all_above_80(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """查询所有科目成绩都在80分以上的优秀学生"""
    data = get_all_above_80_service(db)
    return {"code": 200, "message": "查询成功", "data": data}

@score_router.get("/scores/multiple-fail", response_model=StudentFailResponse, summary="查询不及格超过2次的学生")
def multiple_fail(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """查询不及格次数超过2次的学生及其不及格记录"""
    data = get_multiple_fail_service(db)
    return {"code": 200, "message": "查询成功", "data": data}

@score_router.get("/scores/class-avg", response_model=ClassAvgScoreResponse, summary="查询各班级各次考试平均分统计")
def class_avg(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """统计各班级每次考试的平均分"""
    data = get_class_avg_service(db)
    return {"code": 200, "message": "查询成功", "data": data}
