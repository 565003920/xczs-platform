"""Audit and notification models."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), default="system")
    action = Column(String(100), nullable=False, comment="操作类型")
    entity_type = Column(String(100), comment="实体类型")
    entity_id = Column(Integer, comment="实体ID")
    details = Column(String(500), comment="操作详情")
    ip = Column(String(50), default="127.0.0.1")
    created_at = Column(DateTime, server_default=func.now())


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), default="teacher")
    title = Column(String(200), nullable=False)
    content = Column(String(500))
    is_read = Column(Boolean, default=False)
    event_type = Column(String(50), comment="事件类型")
    created_at = Column(DateTime, server_default=func.now())
