"""Cross-course mode migration — integrated with template library."""
from sqlalchemy.orm import Session
from app.models.teaching import ClassModel, Grade, Observation
from app.models.knowledge import KnowledgeNode, TeachingModeTemplate
from app.services.fingerprint import _match_template, _LABEL_TO_TEMPLATE


def _class_mode_template(db: Session, class_id: int) -> TeachingModeTemplate | None:
    obs = db.query(Observation).filter(Observation.class_id == class_id).all()
    if not obs: return None
    avg_l = sum(o.lecture_ratio for o in obs) / len(obs)
    avg_d = sum(o.discussion_ratio for o in obs) / len(obs)
    avg_p = sum(o.practice_ratio for o in obs) / len(obs)
    if avg_l > 0.6: label = "讲授主导型"
    elif avg_d > 0.5: label = "互动讨论型"
    elif avg_p > 0.4: label = "实践驱动型"
    else: label = "混合型(讲授+互动)"
    return _match_template(db, label, avg_l, avg_p)


def course_similarity(db: Session, course_a_id: int, course_b_id: int) -> float:
    nodes_a = set(n.name for n in db.query(KnowledgeNode).filter(KnowledgeNode.course_id == course_a_id).all())
    nodes_b = set(n.name for n in db.query(KnowledgeNode).filter(KnowledgeNode.course_id == course_b_id).all())
    if not nodes_a or not nodes_b: return 0.0
    return len(nodes_a & nodes_b) / len(nodes_a | nodes_b)


def recommend_migration(db: Session, target_class_id: int) -> dict:
    target = db.query(ClassModel).filter(ClassModel.id == target_class_id).first()
    if not target: raise ValueError("班级不存在")

    target_template = _class_mode_template(db, target_class_id)
    target_mode_name = target_template.name if target_template else "未知"

    all_classes = db.query(ClassModel).filter(ClassModel.id != target_class_id).all()
    candidates = []
    for cls in all_classes:
        cls_grades = [g.score for g in db.query(Grade).filter(Grade.class_id == cls.id).all()]
        cls_avg = sum(cls_grades) / len(cls_grades) if cls_grades else 0
        sim = course_similarity(db, target.course_id, cls.course_id)
        dist_penalty = max(0, 1 - abs((sum(g.score for g in db.query(Grade).filter(Grade.class_id == target_class_id).all()) /
                                       max(len(db.query(Grade).filter(Grade.class_id == target_class_id).all()), 1) - cls_avg) / 50))
        score = round(sim * 0.6 + dist_penalty * 0.4, 2)
        candidates.append({"class_id": cls.id, "class_name": cls.name, "similarity": score, "avg_grade": round(cls_avg, 1)})

    candidates.sort(key=lambda x: x["similarity"], reverse=True)

    recommendations = []
    for c in candidates[:10]:
        src_template = _class_mode_template(db, c["class_id"])
        if not src_template or src_template.name == target_mode_name:
            continue
        recommendations.append({
            "from_class": c["class_name"],
            "mode": src_template.name,
            "mode_description": src_template.description or "",
            "mode_strengths": src_template.strengths or "",
            "mode_stages_count": len(src_template.stages or []),
            "avg_grade": c["avg_grade"],
            "similarity": c["similarity"],
            "reason": f"学情相似度{c['similarity']*100:.0f}%，该班级采用「{src_template.name}」模式，平均分{c['avg_grade']}分"
        })
        if len(recommendations) >= 3: break

    return {
        "target_class_id": target_class_id,
        "target_class_name": target.name,
        "current_mode": target_mode_name,
        "current_template_description": target_template.description if target_template else "",
        "recommendations": recommendations,
    }
