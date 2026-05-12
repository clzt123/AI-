from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from functools import wraps
from jose import jwt, JWTError
from config import SECRET_KEY, ALGORITHM

# 角色权限配置字典
# 角色说明：
# - admin: 管理员，拥有所有模块的完整权限
# - homeroom: 班主任，可管理学生、成绩、就业信息
# - teacher: 任课老师，可查看学生/成绩/班级信息，可录入成绩
ROLE_PERMISSIONS = {
    "student_info": {
        "create": ["admin", "homeroom"],
        "read": ["admin", "homeroom", "teacher"],
        "update": ["admin", "homeroom"],
        "delete": ["admin"],
        "restore": ["admin"]
    },
    "teacher": {
        "create": ["admin"],
        "read": ["admin", "homeroom", "teacher"],
        "update": ["admin"],
        "delete": ["admin"],
        "restore": ["admin"]
    },
    "score": {
        "create": ["admin", "homeroom", "teacher"],
        "read": ["admin", "homeroom", "teacher"],
        "update": ["admin", "homeroom"],
        "delete": ["admin"],
        "restore": ["admin"]
    },
    "class_info": {
        "create": ["admin"],
        "read": ["admin", "homeroom", "teacher"],
        "update": ["admin"],
        "delete": ["admin"],
        "restore": ["admin"]
    },
    "employment": {
        "create": ["admin", "homeroom"],
        "read": ["admin", "homeroom", "teacher"],
        "update": ["admin", "homeroom"],
        "delete": ["admin"],
        "restore": ["admin"]
    },
    "user": {
        "create": ["admin"],
        "read": ["admin", "homeroom", "teacher"],
        "update": ["admin"],
        "delete": ["admin"]
    }
}


class AuthUser:
    def __init__(self, user_id: int, username: str, role: str):
        self.user_id = user_id
        self.username = username
        self.role = role


def get_current_auth_user(authorization: str = Header(...)) -> AuthUser:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="无效的认证格式")
    token = authorization[7:]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or username is None or role is None:
            raise HTTPException(status_code=401, detail="无效的令牌")
        return AuthUser(user_id=user_id, username=username, role=role)
    except JWTError:
        raise HTTPException(status_code=401, detail="令牌验证失败")


def require_permission(module: str, action: str):
    module_names = {
        "student_info": "学生管理",
        "teacher": "教师管理",
        "score": "成绩管理",
        "class_info": "班级管理",
        "employment": "就业管理",
        "user": "用户管理"
    }
    
    action_names = {
        "create": "创建",
        "read": "查看",
        "update": "修改",
        "delete": "删除",
        "restore": "恢复"
    }
    
    role_names = {
        "admin": "管理员",
        "homeroom": "班主任",
        "teacher": "任课老师"
    }
    
    def permission_checker(auth_user: AuthUser = Depends(get_current_auth_user)) -> AuthUser:
        if module not in ROLE_PERMISSIONS:
            raise HTTPException(status_code=403, detail="系统错误：未知的模块配置")
        if action not in ROLE_PERMISSIONS[module]:
            raise HTTPException(status_code=403, detail="系统错误：未知的操作类型")
        
        allowed_roles = ROLE_PERMISSIONS[module][action]
        if auth_user.role not in allowed_roles:
            module_name = module_names.get(module, module)
            action_name = action_names.get(action, action)
            current_role = role_names.get(auth_user.role, auth_user.role)
            allowed_role_names = [role_names.get(r, r) for r in allowed_roles]
            
            if len(allowed_role_names) == 1:
                required_roles = allowed_role_names[0]
            else:
                required_roles = "或".join(allowed_role_names[:-1]) + "或" + allowed_role_names[-1]
            
            raise HTTPException(
                status_code=403,
                detail=f"权限不足：{current_role}无法{action_name}{module_name}，该操作需要{required_roles}权限"
            )
        return auth_user
    return permission_checker
