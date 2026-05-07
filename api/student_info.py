from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas.student_info import *
from typing import Optional
from service.student_info import *

router = APIRouter(prefix="/students", tags=["学生管理"])

# 1 新增：前端不传 id
@router.post("/create", response_model=StudentResponse) #响应体
def add(s: StudentCreate, db: Session = Depends(get_db)): #自动调用get_db，拿到数据库连接，接口结束则自动关闭连接，保证数据库的安全和稳定
    return create_student(db, s)

# 2 列表
@router.get("/check", response_model=StudentListResponse) #分页查询响应体
def list_students(
    student_name: Optional[str] = None,
    class_id: Optional[int] = None,
    page: int=1, page_size:int=10,
    db: Session=Depends(get_db)
):
    total, data = judge_get_students(db, student_name, class_id, page, page_size)
    return {"total":total, "data":data, "page":page, "page_size":page_size} 

# 3 单个查询（用自动生成的 id）
@router.get("/check/{id}", response_model=StudentResponse)
def get_one(id: int, db: Session=Depends(get_db)):
    return judge_get_student(db, id)

# 4 修改
@router.put("/update/{id}", response_model=StudentResponse)
def update(id:int, s:StudentUpdate, db:Session=Depends(get_db)):
    return judge_update_student(db, id, s)

# 5 删除
@router.delete("/delete/{id}")
def remove(id:int, db:Session=Depends(get_db)):
    judge_delete_student(db, id)
    return {"msg":"删除成功"}

#6 恢复学生数据
@router.put("/restore/{id}")
def restore_api(id: int, db:Session=Depends(get_db)):
    judge_restore_student(db, id)
    return {"msg":"恢复成功"}

#7 查询已删除学生
@router.get("/check_is_deleted",response_model=StudentListResponse) #分页查询响应体
def check_is_deleted(
    student_name: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    total, data = judge_get_deleted_student(
        db=db,
        student_name=student_name,
        page=page,
        page_size=page_size
    )
    return {
        "code": 200,
        "msg": "查询成功",
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": data
    }
# 查询所有超过30岁的学员信息
@router.get("/check_age",response_model=List[StudentResponse]) #把传来的多个学生对象转换成json格式的列表
def check_age(db: Session = Depends(get_db)):
    return judge_check_student_age(db)
#统计每个班级的人数以及男生女生人数
@router.get("/check_gender")
def check_gender(db: Session = Depends(get_db)):
    return judge_check_student_gender(db)


