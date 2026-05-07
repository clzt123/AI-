from sqlalchemy.orm import Session
from sqlalchemy import func,case
from models.student_info import Student
from schemas.student_info import StudentCreate, StudentUpdate

# 创建：数据库自动生成id
def create_student(db: Session, s: StudentCreate): #创建数据库会话，导入前端传入的数据
    db_stu = Student(** s.model_dump()) #把前端传入的数据转换成数据库模型，把前端传的json转成字典，**代表解包，导入模型
    db.add(db_stu) #添加到会话
    db.commit() #提交到数据库
    db.refresh(db_stu) #数据库更新
    return db_stu

# 查询按 id（主键）
def get_student(db: Session, id: int):
    return db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first() #返回查询到的第一条数据

# 条件查询
def get_students(db: Session, student_name=None, class_id=None, page=1, page_size=10):
    q = db.query(Student) #查询表
    q = q.filter(Student.is_deleted == 0) #筛选未被删除的
    if student_name:
        q = q.filter(Student.student_name.contains(student_name)) #按照姓名模糊查询
    if class_id:
        q = q.filter(Student.class_id==class_id) #按照班级id查询
    total = q.count() #统计总条数
    data = q.offset((page-1)*page_size).limit(page_size).all() #分页查询当前数据
    return total, data

# 更新按 id
def update_student(db: Session, id: int, data: StudentUpdate):
    stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first() #查询未被删除的学生
    if not stu:
        return None
    for k, v in data.model_dump(exclude_unset=True).items(): #只更新前端传来的字段，对传来的字段进行遍历
        setattr(stu, k, v) #修改前端传来的新值
    db.commit()
    db.refresh(stu) 
    return stu

# if data.student_name:
#     stu.student_name = data.student_name
# if data.age:
#     stu.age = data.age
# if data.gender:
#     stu.gender = data.gender

# 删除按 id
def delete_student(db: Session, id: int):
    stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 0).first()
    if not stu:
        return False
    stu.is_deleted = 1
    db.commit()
    return True

#恢复学生数据
def restore_student(db: Session, id: int):
    stu = db.query(Student).filter(Student.id == id,Student.is_deleted == 1).first()
    if not stu:
        return False
    stu.is_deleted = 0
    db.commit()
    return True

#查询已删除学生的数据
def get_deleted_student(db: Session, student_name=None,page=1, page_size=10):
    q = db.query(Student).filter(Student.is_deleted == 1)
    if student_name:
        q = q.filter(Student.student_name.contains(student_name))
    total = q.count()
    data = q.offset((page-1)*page_size).limit(page_size).all()
    return total, data

# 查询所有超过30岁的学员信息
def check_student_age(db: Session):
    stu_age = db.query(Student).filter(Student.is_deleted == 0,Student.age > 30).all()
    return stu_age

#统计每个班级的人数以及男生女生人数
def check_student_gender(db: Session):
    stu = (db.query(
        Student.class_id.label("班级"),
        func.count(id).label('班级总人数'),
        func.sum(case((Student.gender == "男",1),else_=0)).label("男生人数"), #性别为男则记为1
        func.sum(case((Student.gender == "女",1),else_=0)).label("女生人数")  #性别为女则记为1，最后都是统计总数
    )
    .filter(Student.is_deleted == 0)
    .group_by(Student.class_id)
    .all()) #返回所有班级的统计结果
    return [{
        "班级":s.班级,
        "班级总人数":s.班级总人数,
        "男生人数":s.男生人数,
        "女生人数":s.女生人数
    } for s in stu] #用一个列表推导式的方法将查询到的对象以字典的形式传回前端

