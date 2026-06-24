"""Auth routes + dependency injection."""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User, hash_password, verify_password, create_token, decode_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_token(user.id, user.role)
    return {
        "token": token,
        "user": {"id": user.id, "username": user.username, "display_name": user.display_name, "role": user.role},
    }


@router.get("/me")
def me(user: dict = Depends(lambda: None), db: Session = Depends(get_db),
        authorization: Optional[str] = Header(None)):
    """Get current user info from token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)
    data = decode_token(authorization[7:])
    if not data:
        raise HTTPException(status_code=401)
    u = db.query(User).filter(User.id == data["user_id"]).first()
    if not u:
        raise HTTPException(status_code=401)
    return {"id": u.id, "username": u.username, "display_name": u.display_name, "role": u.role}


# ---- Dependency ----

def get_current_user(authorization: Optional[str] = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="请先登录")
    data = decode_token(authorization[7:])
    if not data:
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    return data
