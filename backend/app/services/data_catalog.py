"""Data asset catalog service."""
from sqlalchemy.orm import Session
from sqlalchemy import func, inspect
from app.database import engine
from app.models.teaching import Course, ClassModel, Student, Grade, Observation, Evaluation
from app.models.knowledge import TeachingModeTemplate, KnowledgeNode


def get_catalog_summary(db: Session) -> dict:
    inspector = inspect(engine)

    entities = {
        "courses": {"model": Course, "label": "课程"},
        "classes": {"model": ClassModel, "label": "班级"},
        "students": {"model": Student, "label": "学生"},
        "grades": {"model": Grade, "label": "成绩"},
        "observations": {"model": Observation, "label": "课堂观察"},
        "evaluations": {"model": Evaluation, "label": "教学评价"},
        "mode_templates": {"model": TeachingModeTemplate, "label": "教学模式"},
        "knowledge_nodes": {"model": KnowledgeNode, "label": "知识点"},
    }

    assets = []
    total_rows = 0
    for key, info in entities.items():
        count = db.query(info["model"]).count()
        total_rows += count
        # Quality: check null rate for key columns
        quality = 100
        try:
            first = db.query(info["model"]).first()
            if first and hasattr(first, "name"):
                null_count = db.query(info["model"]).filter(getattr(info["model"], "name") == None).count()
                quality = round((1 - null_count / max(count, 1)) * 100)
        except:
            pass

        assets.append({
            "type": key,
            "label": info["label"],
            "row_count": count,
            "quality_score": quality,
        })

    assets.sort(key=lambda x: x["row_count"], reverse=True)

    return {
        "total_records": total_rows,
        "entity_count": len(entities),
        "assets": assets,
    }


def get_quality_report(db: Session) -> dict:
    summary = get_catalog_summary(db)
    issues = []
    for a in summary["assets"]:
        if a["quality_score"] < 90:
            issues.append({"type": a["type"], "label": a["label"], "quality": a["quality_score"], "suggestion": f"建议检查{a['label']}数据完整性"})

    return {
        "overall_quality": round(sum(a["quality_score"] for a in summary["assets"]) / max(len(summary["assets"]), 1)),
        "assets": summary["assets"],
        "issues": issues,
    }
