from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Dict, Any, Tuple
from models.score import Score
from models.student_info import Student
from schemas.score import ScoreCreate, ScoreUpdate
from collections import defaultdict

def add_score_dao(db: Session, score: ScoreCreate) -> Score:
    """创建新的成绩记录"""
    try:
        item = Score(**score.model_dump(), is_deleted=0)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise

def check_score_exists(db: Session, student_no: str, exam_order: int) -> Optional[Score]:
    """检查成绩记录是否存在"""
    return db.query(Score).filter(
        Score.student_no == student_no,
        Score.exam_order == exam_order,
        Score.is_deleted == 0
    ).first()

def get_comprehensive_scores(db: Session, id=None, student_no=None, exam_order=None, page=1, page_size=10) -> Tuple[List[Score], int]:
    """综合查询成绩信息，支持多条件筛选和分页"""
    q = db.query(Score).filter(Score.is_deleted == 0)
    if id is not None:
        q = q.filter(Score.id == id)
    if student_no:
        q = q.filter(Score.student_no.like(f"%{student_no}%"))
    if exam_order is not None:
        q = q.filter(Score.exam_order == exam_order)
    total = q.count()
    data_list = q.offset((page - 1) * page_size).limit(page_size).all()
    return data_list, total

def update_score_dao(db: Session, id: int, data: ScoreUpdate) -> Optional[Score]:
    """更新指定成绩记录"""
    try:
        item = db.query(Score).filter_by(id=id, is_deleted=0).first()
        if item:
            item.score = data.score
            db.commit()
            db.refresh(item)
        return item
    except IntegrityError:
        db.rollback()
        raise

def delete_score_dao(db: Session, id: int) -> Optional[Score]:
    """逻辑删除指定成绩记录"""
    try:
        item = db.query(Score).filter_by(id=id, is_deleted=0).first()
        if item:
            item.is_deleted = 1
            db.commit()
        return item
    except IntegrityError:
        db.rollback()
        raise

def get_deleted_scores_dao(db: Session, id: int = None, student_no: str = None, exam_order: int = None) -> List[Score]:
    """查询已删除的成绩记录，支持多条件筛选"""
    query = db.query(Score).filter(Score.is_deleted == 1)

    if id is not None:
        query = query.filter(Score.id.like(f"%{id}%"))
    if student_no:
        query = query.filter(Score.student_no.like(f"%{student_no}%"))
    if exam_order is not None:
        query = query.filter(Score.exam_order.like(f"%{exam_order}%"))

    return query.all()

def restore_scores_dao(db: Session, id: int = None, student_no: str = None, exam_order: int = None) -> List[Score]:
    """恢复已删除的成绩记录"""
    score_list = get_deleted_scores_dao(db, id=id, student_no=student_no, exam_order=exam_order)
    if not score_list:
        return []
    try:
        for score in score_list:
            score.is_deleted = 0
        db.commit()
        return score_list
    except IntegrityError:
        db.rollback()
        raise

# 查询每次考核成绩大于80的学生
# 业务需求：找出所有科目成绩都在80分以上的优秀学生
# 关键逻辑：先按学号分组找出每个学生的最低分，再筛选最低分>80的学生
def get_all_above_80_dao(db: Session) -> List[Dict[str, Any]]:
    """查询所有考核成绩都大于80分的学生"""
    # 子查询：按学号分组，查询每个学生的最低分
    subquery = db.query(
        Score.student_no,
        func.min(Score.score).label("min_score")
    ).filter(Score.is_deleted == 0).group_by(Score.student_no).subquery()

    # 主查询：关联学生表，查询最低分>80的学生信息
    result = db.query(
        Student.student_no,
        Student.student_name,
        subquery.c.min_score.label("score")
    ).join(
        subquery, Student.student_no == subquery.c.student_no
    ).filter(
        subquery.c.min_score > 80,
        Student.is_deleted == 0
    ).all()

    # 将查询结果转成字典列表，适配前端格式
    return [
        {"student_no": r[0], "student_name": r[1], "score": r[2]}
        for r in result
    ]

# 查询不及格超过2次的学生
# 业务需求：找出多次不及格需要重点关注的学生
# 关键逻辑：先筛选不及格记录，按学号分组统计次数，再联表查询详细信息
def get_multiple_fail_dao(db: Session) -> List[Dict[str, Any]]:
    """查询不及格次数超过2次的学生"""
    # 1. 找出不及格 > 2 次的学号
    fail_student_nos = db.query(Score.student_no).filter(
        Score.score < 60,
        Score.is_deleted == 0
    ).group_by(Score.student_no).having(func.count() > 2)
    if not fail_student_nos.count():
        return []
    # 2. 查询这些学生的姓名 + 所有不及格记录
    query = db.query(
        Student.student_no,
        Student.student_name,
        Score.exam_order,
        Score.score
    ).join(
        Score,
        Student.student_no == Score.student_no
    ).filter(
        Student.student_no.in_(fail_student_nos),
        Score.score < 60,
        Student.is_deleted == 0,
        Score.is_deleted == 0
    )
    # 3. 按学生分组
    result = defaultdict(lambda: {"student_name": "", "fail_records": []})
    for row in query.all():
        result[row.student_no]["student_no"] = row.student_no
        result[row.student_no]["student_name"] = row.student_name
        result[row.student_no]["fail_records"].append(
            {"exam_order": row.exam_order,
             "score": float(row.score)
             }
        )
    # 4. 返回最终格式
    return list(result.values())


# 按考核序次和班级分组，统计每个班级每场考试的平均分
# 业务需求：分析各班级在各次考试中的平均表现
# 关键逻辑：关联学生表获取班级信息，按考试序号+班级分组计算平均分
def get_class_avg_dao(db: Session) -> List[Dict[str, Any]]:
    """统计每个班级每次考试的平均分"""
    # 关联学生表，分组计算班级+考试平均分
    query = (
        db.query(
            Student.class_id,  # 班级ID
            Score.exam_order,  # 考试序号
            func.avg(Score.score).label("avg_score")  # 平均分
        )
        .join(Student, Score.student_no == Student.student_no)  # 关联学生
        .filter(Student.is_deleted == 0, Score.is_deleted == 0)  # 过滤未删除数据
        .group_by(Score.exam_order, Student.class_id)  # 分组条件
    )
    # 将结果转为字典列表
    return [
        {"class_id": r[0],"exam_order":r[1], "avg_score": float(r[2]) if r[2] else None}
        for r in query.all()
    ]