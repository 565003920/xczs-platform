"""User model and auth utilities."""
import hashlib, os, time, json, base64
from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

SECRET_KEY = "xczs-secret-key-2026"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    display_name = Column(String(100), comment="显示名称")
    role = Column(String(20), default="teacher", comment="teacher/admin")
    created_at = Column(DateTime, server_default=func.now())


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hash_val: str) -> bool:
    return hash_password(password) == hash_val


def create_token(user_id: int, role: str) -> str:
    """Simple JWT-like token (HMAC + base64)."""
    header = base64.urlsafe_b64encode(json.dumps({"alg": "HS256", "typ": "JWT"}).encode()).decode().rstrip("=")
    payload = base64.urlsafe_b64encode(json.dumps({
        "user_id": user_id, "role": role, "exp": int(time.time()) + 86400 * 7
    }).encode()).decode().rstrip("=")
    signature = hashlib.sha256(f"{header}.{payload}.{SECRET_KEY}".encode()).hexdigest()[:32]
    return f"{header}.{payload}.{signature}"


def decode_token(token: str) -> dict | None:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header, payload, signature = parts
        expected = hashlib.sha256(f"{header}.{payload}.{SECRET_KEY}".encode()).hexdigest()[:32]
        if signature != expected:
            return None
        # Add padding for base64 decode
        payload += "=" * (4 - len(payload) % 4) if len(payload) % 4 else ""
        data = json.loads(base64.urlsafe_b64decode(payload))
        if data.get("exp", 0) < time.time():
            return None
        return data
    except Exception:
        return None
