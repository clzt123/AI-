from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import re


class UserRegister(BaseModel):
    username: str
    password: str
    role: str
    real_name: Optional[str] = None
    phone: Optional[str] = None

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v or len(v.strip()) == 0:
            raise ValueError('用户名不能为空')
        if len(v) < 3 or len(v) > 20:
            raise ValueError('用户名长度必须在3-20个字符之间')
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', v):
            raise ValueError('用户名只能包含字母、数字、下划线和中文')
        return v.strip()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v or len(v) == 0:
            raise ValueError('密码不能为空')
        if len(v) < 6:
            raise ValueError('密码长度不能少于6个字符')
        if len(v) > 50:
            raise ValueError('密码长度不能超过50个字符')
        if not re.search(r'[a-zA-Z]', v):
            raise ValueError('密码必须包含至少一个字母')
        if not re.search(r'\d', v):
            raise ValueError('密码必须包含至少一个数字')
        return v

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        valid_roles = ['admin', 'homeroom', 'teacher']
        if v not in valid_roles:
            raise ValueError(f'无效的角色，可选值: {", ".join(valid_roles)}')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v.strip()) > 0:
            if not re.match(r'^1[3-9]\d{9}$', v):
                raise ValueError('手机号格式不正确，请输入11位有效手机号')
            return v.strip()
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    role: str
    real_name: Optional[str]
    phone: Optional[str]
    create_time: Optional[datetime]

    class Config:
        from_attributes = True
