from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from models.user import User
from schemas.user import UserRegister


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """根据用户名查询用户"""
    return db.query(User).filter(
        User.username == username,
        User.is_deleted == 0
    ).first()


def create_user(db: Session, data: UserRegister, password_hash: str) -> User:
    """创建新用户"""
    try:
        user = User(
            username=data.username,
            password_hash=password_hash,
            role=data.role,
            real_name=data.real_name,
            phone=data.phone
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except SQLAlchemyError:
        db.rollback()
        raise


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """根据用户ID查询用户"""
    return db.query(User).filter(
        User.user_id == user_id,
        User.is_deleted == 0
    ).first()
