from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from service.user import register_service, login_service, get_current_user
from service.auth import require_permission, AuthUser
from schemas.user import UserRegister, UserLogin, UserResponse
from typing import Dict, Any

user_router = APIRouter()


@user_router.post('/register', response_model=dict, summary="用户注册")
def register(data: UserRegister, db: Session = Depends(get_db), _: AuthUser = Depends(require_permission("user", "create"))) -> Dict[str, Any]:
    """用户注册接口，仅管理员可注册新用户"""
    user = register_service(db, data)
    return {"code": 200, "message": "注册成功", "data": user.model_dump()}


@user_router.post('/login', response_model=dict, summary="用户登录")
def login(data: UserLogin, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """用户登录接口，返回JWT令牌和用户信息"""
    result = login_service(db, data.username, data.password)
    return {"code": 200, "message": "登录成功", "data": result}


@user_router.get('/me', response_model=dict, summary="获取当前用户信息")
def get_me(token: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """根据JWT令牌获取当前登录用户信息"""
    user = get_current_user(db, token)
    return {"code": 200, "message": "查询成功", "data": user.model_dump()}
