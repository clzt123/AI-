from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from dao.user import get_user_by_username, create_user, get_user_by_id
from schemas.user import UserRegister, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=4)

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

VALID_ROLES = ["admin", "homeroom", "teacher"]


def hash_password(password: str) -> str:
    """对密码进行哈希加密"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码是否正确"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建JWT访问令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def register_service(db: Session, data: UserRegister) -> UserResponse:
    """用户注册，检查用户名和角色合法性"""
    if data.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail=f"无效的角色，可选角色: {', '.join(VALID_ROLES)}")

    if get_user_by_username(db, data.username):
        raise HTTPException(status_code=409, detail="用户名已存在")

    password_hash = hash_password(data.password)
    user = create_user(db, data, password_hash)
    return UserResponse.model_validate(user)


def login_service(db: Session, username: str, password: str) -> dict:
    """用户登录，验证用户名和密码"""
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    access_token = create_access_token(data={"sub": user.username, "role": user.role, "user_id": user.user_id})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user).model_dump()
    }


def get_current_user(db: Session, token: str) -> UserResponse:
    """根据JWT令牌获取当前用户信息"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="无效的令牌")
    except JWTError:
        raise HTTPException(status_code=401, detail="令牌验证失败")

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return UserResponse.model_validate(user)
