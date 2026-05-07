from pydantic import BaseModel,Field,ConfigDict
from typing import Optional,List
from datetime import date

class StudentCreate(BaseModel):
    student_no:str = Field(...,description="学生编号（必填）")
    class_id:int = Field(...,description="班级id（必填）")
    student_name:str = Field(...,description="学生姓名（必填）")
    gender:Optional[str] = Field(None,description="性别（选填）")
    age:Optional[int] = Field(None,description="年龄（选填）")
    native_place:Optional[str]=Field(None,description="籍贯（）选填")
    graduate_school: Optional[str] = Field(None, description="毕业院校（选填）")
    major: Optional[str] = Field(None, description="专业（选填）")
    education: Optional[str] = Field(None, description="学历（选填）")
    admission_time: Optional[date] = Field(None, description="入学时间（选填）")
    graduate_time: Optional[date] = Field(None, description="毕业时间（选填）")
    advisor_id: Optional[int] = Field(None, description="顾问编号（选填）")

class StudentUpdate(BaseModel):
    student_no: Optional[str] = Field(None, description="学生编号（选填）")
    class_id: Optional[int] = Field(None, description="班级ID（选填）")
    student_name: Optional[str] = Field(None, description="学生姓名（选填）")
    gender: Optional[str] = Field(None, description="性别（选填）")
    age: Optional[int] = Field(None, description="年龄（选填）")
    native_place: Optional[str] = Field(None, description="籍贯（选填）")
    graduate_school: Optional[str] = Field(None, description="毕业院校（选填）")
    major: Optional[str] = Field(None, description="专业（选填）")
    education: Optional[str] = Field(None, description="学历（选填）")
    admission_time: Optional[date] = Field(None, description="入学时间（选填）")
    graduate_time: Optional[date] = Field(None, description="毕业时间（选填）")
    advisor_id: Optional[int] = Field(None, description="顾问编号（选填）")


class StudentResponse(BaseModel):
    id: int = Field(..., description="数据库主键ID")
    student_no: str = Field(..., description="学生编号")
    class_id: int = Field(..., description="班级ID")
    student_name: str = Field(..., description="学生姓名")
    gender: Optional[str] = Field(None, description="性别")
    age: Optional[int] = Field(None, description="年龄")
    native_place: Optional[str] = Field(None, description="籍贯")
    graduate_school: Optional[str] = Field(None, description="毕业院校")
    major: Optional[str] = Field(None, description="专业")
    education: Optional[str] = Field(None, description="学历")
    admission_time: Optional[date] = Field(None, description="入学时间")
    graduate_time: Optional[date] = Field(None, description="毕业时间")
    advisor_id: Optional[int] = Field(None, description="顾问编号")
    is_deleted: int = Field(0, description="逻辑删除标记")

    # 修复：Config 类必须缩进到 StudentResponse 内部！
    class Config:
        from_attributes = True


# class BaseSchema(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

# class StudentQuery(BaseModel):
#     keyword:Optional[str] = Field(None,description="关键词：姓名或学号")
#     class_id:Optional[int] = Field(None,description="按班级筛选")
#     gender:Optional[str] = Field(None,description="按性别筛选")
#     page:int = Field(1,description="页码，默认第一页")
#     page_size:int = Field(10,description="每页数量，默认10条")


# class StudentListResponse(BaseModel):
#     total:int
#     items:List[StudentResponse]


