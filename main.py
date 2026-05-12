from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from database import engine,Base
from api import class_router, employment_router, score_router, student_info_router, teacher_router, user_router
import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from config import APP_HOST, APP_PORT

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
app = FastAPI(title="学生管理系统",version="2.0")

ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "code": 422,
            "message": "请求参数校验失败",
            "data": None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": "服务器内部错误",
            "data": None
        }
    )

# 挂载静态文件
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

# 导入子路由（添加/api前缀）
app.include_router(user_router, prefix="/auth", tags=["用户认证"])
app.include_router(student_info_router, prefix="/api", tags=["学生管理"])
app.include_router(score_router, prefix="/api", tags=["学生成绩"])
app.include_router(employment_router, prefix="/api", tags=["就业管理"])
app.include_router(teacher_router, prefix="/api", tags=["老师管理模块"])
app.include_router(class_router, prefix="/api", tags=["班级管理"])

# 前端页面路由
@app.get("/")
async def index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/login/")
async def page_login():
    return FileResponse(os.path.join(frontend_dir, "auth.html"))

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
    from config import APP_HOST, APP_PORT
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)