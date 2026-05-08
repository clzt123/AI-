from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from service.score import *
from schemas.score import *
from database import get_db

# 创建成绩模块路由实例，用于注册成绩相关接口
score_router = APIRouter()

# 添加单条成绩信息（无需传id，数据库自增）
@score_router.post('/scores', response_model=ScoreResponse, summary="添加成绩")
def add_score(score: ScoreCreate, db: Session = Depends(get_db)):
    # 调用业务逻辑层添加成绩方法，传入数据库会话和成绩参数
    result = add_score_service(db, score)
    # 返回统一响应格式：状态码、提示信息、返回数据
    return {"code": 200, "message": "添加成功", "data": result}

# 综合查询成绩
# 功能：支持按id/学号/考试序号查询 + 分页查询
@score_router.get('/scores', response_model=Score_Page_Response, summary="综合查询成绩")
def get_scores(
    # 成绩ID查询参数，可选，最小值1
    id: int | None = Query(None, description="成绩ID", ge=1),
    # 学生学号查询参数，可选，长度1-20
    student_no: str | None = Query(None, description="学生学号", min_length=1, max_length=20),
    # 考试序号查询参数，可选，最小值1
    exam_order: int | None = Query(None, description="考试序号", ge=1),
    # 分页页码，默认1，最小值1
    page: int = Query(1, description="页码", ge=1),
    # 每页条数，默认10，范围1-50
    size: int = Query(10, description="每页条数", ge=1, le=50),
    # 依赖注入获取数据库会话
    db: Session = Depends(get_db)
):
    # 只调用 service 层处理业务逻辑，不直接操作数据库
    result = get_scores_service(db, id, student_no, exam_order, page, size)
    # 返回查询结果
    return result

# 修改成绩接口
@score_router.put("/scores/{id}", summary="修改成绩")
def update_score(id: int, update_data: ScoreUpdate, db: Session = Depends(get_db)):
    # 调用业务逻辑层修改成绩方法，传入id、修改数据、数据库会话
    data = update_score_service(db, id, update_data)
    # 返回修改成功响应
    return {"code":200,"message":"修改成功","data":data}

# 删除成绩接口
@score_router.delete("/scores/{id}", summary="删除成绩")
def delete_score(id: int, db: Session = Depends(get_db)):
    # 调用业务逻辑层删除成绩方法（逻辑删除）
    delete_score_service(db, id)
    # 返回删除成功响应
    return {"code":200,"message":"删除成功"}

# 恢复已删除的成绩
@score_router.put("/scores/delete/restore", summary="批量/单条恢复已删除成绩")
def restore_score(
    id: int = None,               # 可选
    student_no: str = None,       # 可选
    exam_order: int = None,       # 可选
    db: Session = Depends(get_db)
):
    count = restore_score_service(db, id, student_no, exam_order)
    return {"code": 200, "message": f"恢复成功，共恢复 {count} 条"}

# 统计：所有科目80分以上的学生
@score_router.get("/scores/all-above-80", summary="查询80分以上学生")
def all_above_80(db: Session = Depends(get_db)):
    # 调用业务逻辑层获取所有科目80分以上学生数据
    data = get_all_above_80_service(db)
    # 返回查询成功响应
    return {"code": 200, "message": "查询成功", "data": data}

# 查询不及格次数超过2次的学生
@score_router.get("/scores/multiple-fail", response_model=StudentFailResponse, summary="查询不及格超过2次的学生")
def multiple_fail(db: Session = Depends(get_db)):
    # 调用业务逻辑层获取不及格超过2次的学生数据
    data = get_multiple_fail_service(db)
    # 返回查询成功响应
    return {"code": 200, "message": "查询成功", "data": data}

# 按考试+班级分组，统计各班级各考试的平均分
@score_router.get("/scores/class-avg", response_model=ClassAvgScoreResponse, summary="查询各班级各次考试平均分统计")
def class_avg(db: Session = Depends(get_db)):
    # 调用业务逻辑层获取班级平均分统计数据
    data = get_class_avg_service(db)
    # 返回查询成功响应
    return {"code": 200, "message": "查询成功", "data": data}
