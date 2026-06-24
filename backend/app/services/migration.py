"""Cross-course teaching mode migration engine."""
from sqlalchemy.orm import Session
from app.models.teaching import ClassModel, Grade, Observation
from app.models.knowledge import KnowledgeNode, TeachingModeTemplate


def course_similarity(db: Session, course_a_id: int, course_b_id: int) -> float:
    """Compute course similarity based on knowledge graph overlap (0-1)."""
    nodes_a = set(n.name for n in db.query(KnowledgeNode).filter(KnowledgeNode.course_id == course_a_id).all())
    nodes_b = set(n.name for n in db.query(KnowledgeNode).filter(KnowledgeNode.course_id == course_b_id).all())
    if not nodes_a or not nodes_b:
        return 0.0
    intersection = nodes_a & nodes_b
    union = nodes_a | nodes_b
    return len(intersection) / len(union)


def find_similar_classes(db: Session, class_id: int, limit: int = 5) -> list[dict]:
    """Find classes similar to the target class based on grade distribution."""
    target = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if not target:
        raise ValueError("班级不存在")

    target_grades = [g.score for g in db.query(Grade).filter(Grade.class_id == class_id).all()]
    target_avg = sum(target_grades) / len(target_grades) if target_grades else 0

    all_classes = db.query(ClassModel).filter(ClassModel.id != class_id).all()
    results = []
    for cls in all_classes:
        cls_grades = [g.score for g in db.query(Grade).filter(Grade.class_id == cls.id).all()]
        cls_avg = sum(cls_grades) / len(cls_grades) if cls_grades else 0
        sim = course_similarity(db, target.course_id, cls.course_id)
        dist = abs(target_avg - cls_avg)
        score = round(sim * 0.6 + max(0, 1 - dist / 50) * 0.4, 2)
        results.append({"class_id": cls.id, "class_name": cls.name, "similarity": score, "avg_grade": round(cls_avg, 1)})

    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:limit]


def recommend_migration(db: Session, target_class_id: int) -> dict:
    """Recommend teaching modes from similar classes that have good results."""
    target = db.query(ClassModel).filter(ClassModel.id == target_class_id).first()
    if not target:
        raise ValueError("班级不存在")

    similar = find_similar_classes(db, target_class_id, limit=5)
    target_obs = db.query(Observation).filter(Observation.class_id == target_class_id).all()
    target_mode = target_obs[0].teaching_style_label if target_obs else "未知"

    recommendations = []
    for sim in similar:
        obs_list = db.query(Observation).filter(Observation.class_id == sim["class_id"]).all()
        if not obs_list:
            continue
        mode_label = obs_list[0].teaching_style_label or "未知"
        if mode_label == target_mode:
            continue
        grades = [g.score for g in db.query(Grade).filter(Grade.class_id == sim["class_id"]).all()]
        avg_g = sum(grades) / len(grades) if grades else 0
        recommendations.append({
            "from_class": sim["class_name"],
            "mode": mode_label,
            "avg_grade": round(avg_g, 1),
            "similarity": sim["similarity"],
            "reason": f"学情相似度{sim['similarity']*100:.0f}%，该模式在该班级平均分{avg_g:.1f}",
        })

    recommendations.sort(key=lambda x: x["avg_grade"], reverse=True)
    return {"target_class_id": target_class_id, "target_class_name": target.name, "current_mode": target_mode, "recommendations": recommendations[:3]}
