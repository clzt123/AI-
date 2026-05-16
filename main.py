from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import course, event

app = FastAPI(title="粤教服务智能客服API", version="1.0.0")

# 配置CORS（允许Dify跨域调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境替换为你的Dify域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(course.router, prefix="/api/course", tags=["课程项目"])
app.include_router(event.router, prefix="/api/event", tags=["活动讲座"])

@app.get("/")
def read_root():
    return {"message": "粤教服务智能客服API运行正常"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
