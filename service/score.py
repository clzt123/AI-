from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from dao.score import *
from schemas.score import ScoreCreate, ScoreUpdate

def add_score_service(db, score: ScoreCreate):
    exists = check_score_exists(db, score.student_no, score.exam_order)
    if exists:
        raise HTTPException(
            status_code=409,
            detail="该学生此考试成绩已存在，不可重复添加"
        )
    return add_score_dao(db, score)

def format_score_list(score_list):
    return [
        {
            "id": s.id,
            "student_no": s.student_no,
            "exam_order": s.exam_order,
            "score": float(s.score) if s.score else None
        }
        for s in score_list
    ]

def get_scores_service(db, id, student_no, exam_order, page, size):
    page = max(1, page)
    size = max(1, min(size, 50))
    data_list, total = get_comprehensive_scores(db, id, student_no, exam_order, page, size)
    result_data = format_score_list(data_list)
    return {
        "code": 200,
        "message": "查询成功" if result_data else "暂无成绩数据",
        "data": result_data,
        "total": total,
        "page": page,
        "size": size
    }

def update_score_service(db, id: int, data: ScoreUpdate):
    item = update_score_dao(db, id, data)
    if not item:
        raise HTTPException(status_code=404, detail="成绩不存在")
    return item

def delete_score_service(db, id: int):
    item = delete_score_dao(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="成绩不存在")
    return True

def restore_score_service(db: Session, id: int = None, student_no: str = None, exam_order: int = None):
    score_list = get_deleted_scores_dao(db, id=id, student_no=student_no, exam_order=exam_order)
    if not score_list:
        raise HTTPException(status_code=404, detail="未找到任何已删除的成绩数据")
    try:
        for score in score_list:
            score.is_deleted = 0
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="恢复操作失败，数据库错误")
    return len(score_list)

def get_all_above_80_service(db):
    data = get_all_above_80_dao(db)
    if not data:
        raise HTTPException(status_code=404, detail="暂无80分以上学生")
    return data

def get_multiple_fail_service(db):
    data = get_multiple_fail_dao(db)
    if not data:
        raise HTTPException(status_code=404, detail="暂无不及格超过2次的学生")
    return data

def get_class_avg_service(db):
    data = get_class_avg_dao(db)
    if not data:
        raise HTTPException(status_code=404, detail="暂无考试成绩数据")
    return data