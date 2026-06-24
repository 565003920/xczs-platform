"""Knowledge graph and teaching mode template models."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func, JSON
from sqlalchemy.orm import relationship

from app.database import Base


class TeachingModeTemplate(Base):
    __tablename__ = "teaching_mode_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="模式名称")
    category = Column(String(50), comment="分类：内置/自定义")
    description = Column(String(1000), comment="模式描述")
    stages = Column(JSON, comment="教学环节定义 [{name, duration, activity_type, teacher_action, student_action}]")
    suitable_scenarios = Column(String(500), comment="适用场景")
    strengths = Column(String(500), comment="优势")
    limitations = Column(String(500), comment="局限")
    created_by = Column(String(100), default="system", comment="创建者")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True, comment="关联课程（自定义模式）")
    usage_count = Column(Integer, default=0, comment="使用次数")
    avg_rating = Column(Float, default=0.0, comment="平均评分")
    created_at = Column(DateTime, server_default=func.now())


class KnowledgeNode(Base):
    __tablename__ = "knowledge_nodes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="知识点名称")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("knowledge_nodes.id"), nullable=True, comment="父节点（章节）")
    difficulty = Column(Float, default=3.0, comment="难度系数 1-5")
    order_index = Column(Integer, default=0, comment="排序")
    created_at = Column(DateTime, server_default=func.now())

    course = relationship("Course")
    children = relationship("KnowledgeNode", backref="parent", remote_side=[id])


class KnowledgeEdge(Base):
    __tablename__ = "knowledge_edges"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("knowledge_nodes.id"), nullable=False)
    target_id = Column(Integer, ForeignKey("knowledge_nodes.id"), nullable=False)
    relation_type = Column(String(50), default="prerequisite", comment="关系类型: prerequisite/parallel/contains")
    created_at = Column(DateTime, server_default=func.now())

    source = relationship("KnowledgeNode", foreign_keys=[source_id])
    target = relationship("KnowledgeNode", foreign_keys=[target_id])
