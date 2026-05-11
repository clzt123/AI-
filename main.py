from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from database import engine,Base
from api import class_router, employment_router, score_router, student_info_router, teacher_router
import os
from dotenv import load_dotenv

load_dotenv()

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

#删除所有表
# Base.metadata.drop_all(bind=engine)
#创建表
Base.metadata.create_all(bind=engine)
# 创建系统
app = FastAPI(title="学生管理系统",version="2.0")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return {
        "code": exc.status_code,
        "message": exc.detail,
        "data": None
    }

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return {
        "code": 422,
        "message": "请求参数校验失败",
        "data": [str(err) for err in exc.errors()]
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "code": 500,
        "message": "服务器内部错误",
        "data": None
    }

# 挂载静态文件
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# 导入子路由（添加/api前缀）
app.include_router(student_info_router, prefix="/api", tags=["学生管理"])
app.include_router(score_router, prefix="/api", tags=["学生成绩"])
app.include_router(employment_router, prefix="/api", tags=["就业管理"])
app.include_router(teacher_router, prefix="/api", tags=["老师管理模块"])
app.include_router(class_router, prefix="/api", tags=["班级管理"])

# 前端页面路由
@app.get("/")
async def index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/pages/student/")
async def page_student():
    return FileResponse(os.path.join(frontend_dir, "pages", "student", "index.html"))

@app.get("/pages/score/")
async def page_score():
    return FileResponse(os.path.join(frontend_dir, "pages", "score", "index.html"))

@app.get("/pages/employment/")
async def page_employment():
    return FileResponse(os.path.join(frontend_dir, "pages", "employment", "index.html"))

@app.get("/pages/teacher/")
async def page_teacher():
    return FileResponse(os.path.join(frontend_dir, "pages", "teacher", "index.html"))

@app.get("/pages/class/")
async def page_class():
    return FileResponse(os.path.join(frontend_dir, "pages", "class", "index.html"))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)