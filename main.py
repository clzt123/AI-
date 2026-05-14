from fastapi import FastAPI
from api.student_routes import router
from core.config import settings

app = FastAPI(
    title="Dify HTTP Request Service",
    description="用于对接 Dify 的后端服务，提供数据库 CRUD 和动态 SQL 查询功能",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1/osa")

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Dify HTTP Request Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )