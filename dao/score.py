from sqlalchemy import func
from sqlalchemy.orm import Session

from database import *
from models.score import Score_DB
from models.student_info import Student
from schemas.score import ScoreCreate, ScoreUpdate
from collections import defaultdict

def add_score_dao(db: Session, score: ScoreCreate):
    item = Score_DB(**score.model_dump(), is_deleted=0)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def check_score_exists(db: Session, student_no: str, exam_order: int):
    return db.query(Score_DB).filter(
        Score_DB.student_no == student_no,
        Score_DB.exam_order == exam_order,
        Score_DB.is_deleted == 0
    ).first()

def get_comprehensive_scores(db: Session, id=None, student_no=None, exam_order=None, page=1, size=10):
    q = db.query(Score_DB).filter(Score_DB.is_deleted == 0)
    if id:
        q = q.filter(Score_DB.id.like(f"%{id}%"))
    if student_no:
        q = q.filter(Score_DB.student_no.like(f"%{student_no}%"))
    if exam_order:
        q = q.filter(Score_DB.exam_order.like(f"%{exam_order}%"))
    total = q.count()
    data_list = q.offset((page - 1) * size).limit(size).all()
    return data_list, total

def update_score_dao(db: Session, id: int, data: ScoreUpdate):
    item = db.query(Score_DB).filter_by(id=id, is_deleted=0).first()
    if item:
        item.score = data.score
        db.commit()
        db.refresh(item)
    return item

def delete_score_dao(db: Session, id: int):
    item = db.query(Score_DB).filter_by(id=id, is_deleted=0).first()
    if item:
        item.is_deleted = 1
        db.commit()
    return item

def get_deleted_scores_dao(db: Session, id: int = None, student_no: str = None, exam_order: int = None):
    query = db.query(Score_DB).filter(Score_DB.is_deleted == 1)

    if id is not None:
        query = query.filter(Score_DB.id.like(f"%{id}%"))
    if student_no:
        query = query.filter(Score_DB.student_no.like(f"%{student_no}%"))
    if exam_order is not None:
        query = query.filter(Score_DB.exam_order.like(f"%{exam_order}%"))

    return query.all()

# 查询每次考核成绩大于80的学生
def get_all_above_80_dao(db: Session):
    # 子查询：按学号分组，查询每个学生的最低分
    subquery = db.query(
        Score_DB.student_no,
        func.min(Score_DB.score).label("min_score")
    ).filter(Score_DB.is_deleted == 0).group_by(Score_DB.student_no).subquery()

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
def get_multiple_fail_dao(db: Session):
    # 1. 找出不及格 > 2 次的学号
    fail_student_nos = db.query(Score_DB.student_no).filter(
        Score_DB.score < 60,
        Score_DB.is_deleted == 0
    ).group_by(Score_DB.student_no).having(func.count() > 2)  # 查询不及格大于2次的学生学号
    if not fail_student_nos.count():  # 如果没有符合条件的数据
        return []  # 直接返回空列表
    # 2. 查询这些学生的姓名 + 所有不及格记录
    query = db.query(
        Student.student_no,
        Student.student_name,
        Score_DB.exam_order,
        Score_DB.score
    ).join(
        Score_DB,
        Student.student_no == Score_DB.student_no
    ).filter(
        Student.student_no.in_(fail_student_nos),
        Score_DB.score < 60,
        Student.is_deleted == 0,
        Score_DB.is_deleted == 0
    )  # 联表查询学生信息与不及格成绩
    # 3. 按学生分组
    result = defaultdict(lambda: {"student_name": "", "fail_records": []})  # 创建自动初始化字典
    for row in query.all():  # 遍历所有不及格记录
        result[row.student_no]["student_no"] = row.student_no  # 设置学生学号
        result[row.student_no]["student_name"] = row.student_name  # 设置学生姓名
        result[row.student_no]["fail_records"].append(
            {"exam_order": row.exam_order,
             "score": float(row.score)
             }
        )  # 添加不及格记录
    # 4. 返回最终格式
    return list(result.values())  # 将字典值转为列表返回


# 按考核序次和班级分组，统计每个班级每场考试的平均分
def get_class_avg_dao(db: Session):
    # 关联学生表，分组计算班级+考试平均分
    query = (
        db.query(
            Student.class_id,  # 班级ID
            Score_DB.exam_order,  # 考试序号
            func.avg(Score_DB.score).label("avg_score")  # 平均分
        )
        .join(Student, Score_DB.student_no == Student.student_no)  # 关联学生
        .filter(Student.is_deleted == 0, Score_DB.is_deleted == 0)  # 过滤未删除数据
        .group_by(Score_DB.exam_order, Student.class_id)  # 分组条件
    )
    # 将结果转为字典列表
    return [
        {"class_id": r[0],"exam_order":r[1], "avg_score": float(r[2]) if r[2] else None}
        for r in query.all()
    ]