"""Teaching mode template management."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import random

from app.database import get_db
from app.models.knowledge import TeachingModeTemplate, KnowledgeNode, KnowledgeEdge
from app.models.teaching import ClassModel
from app.services.knowledge_graph import get_course_knowledge_graph

router = APIRouter(prefix="/api/modes", tags=["modes"])


# ===== Mode Templates =====

@router.get("/templates")
def list_templates(category: str = None, db: Session = Depends(get_db)):
    q = db.query(TeachingModeTemplate)
    if category:
        q = q.filter(TeachingModeTemplate.category == category)
    return q.all()


@router.get("/templates/{mode_id}")
def get_template(mode_id: int, db: Session = Depends(get_db)):
    mode = db.query(TeachingModeTemplate).filter(TeachingModeTemplate.id == mode_id).first()
    if not mode:
        raise HTTPException(status_code=404, detail="模式不存在")
    return mode


# ===== Custom Modes =====

@router.post("/custom")
def create_custom(mode: dict, db: Session = Depends(get_db)):
    t = TeachingModeTemplate(
        name=mode.get("name", ""),
        category="custom",
        description=mode.get("description", ""),
        stages=mode.get("stages", []),
        suitable_scenarios=mode.get("suitable_scenarios", ""),
        strengths=mode.get("strengths", ""),
        limitations=mode.get("limitations", ""),
        created_by=mode.get("created_by", "teacher"),
        course_id=mode.get("course_id", None),
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


@router.get("/custom")
def list_custom(course_id: int = None, db: Session = Depends(get_db)):
    q = db.query(TeachingModeTemplate).filter(TeachingModeTemplate.category == "custom")
    if course_id:
        q = q.filter(TeachingModeTemplate.course_id == course_id)
    return q.all()


@router.put("/custom/{mode_id}")
def update_custom(mode_id: int, mode: dict, db: Session = Depends(get_db)):
    t = db.query(TeachingModeTemplate).filter(
        TeachingModeTemplate.id == mode_id,
        TeachingModeTemplate.category == "custom"
    ).first()
    if not t:
        raise HTTPException(status_code=404, detail="自定义模式不存在")
    for key in ["name", "description", "stages", "suitable_scenarios", "strengths", "limitations"]:
        if key in mode:
            setattr(t, key, mode[key])
    db.commit()
    return t


@router.delete("/custom/{mode_id}")
def delete_custom(mode_id: int, db: Session = Depends(get_db)):
    t = db.query(TeachingModeTemplate).filter(
        TeachingModeTemplate.id == mode_id,
        TeachingModeTemplate.category == "custom"
    ).first()
    if not t:
        raise HTTPException(status_code=404, detail="自定义模式不存在")
    db.delete(t)
    db.commit()
    return {"ok": True}


# ===== Mode Recommendation =====

@router.get("/recommend")
def recommend_modes(class_id: int = None, db: Session = Depends(get_db)):
    """Recommend teaching modes based on class profile."""
    templates = db.query(TeachingModeTemplate).filter(TeachingModeTemplate.category == "builtin").all()
    if not templates:
        return {"class_id": class_id, "recommendations": []}

    # Simple recommendation: random order for now (will be profile-driven in v2.0)
    shuffled = list(templates)
    random.shuffle(shuffled)
    recs = []
    for t in shuffled[:3]:
        strengths = []
        if t.suitable_scenarios:
            strengths.append(t.suitable_scenarios)
        if t.strengths:
            strengths.append(t.strengths)
        recs.append({
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "reasons": strengths[:2],
            "stages_preview": [s.get("name", "") for s in (t.stages or [])[:4]],
        })
    return {"class_id": class_id, "recommendations": recs}


# ===== Knowledge Graph =====

@router.get("/knowledge-graph")
def knowledge_graph(course_id: int, db: Session = Depends(get_db)):
    return get_course_knowledge_graph(db, course_id)
