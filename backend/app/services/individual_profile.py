"""Individual student learning profile."""
from sqlalchemy.orm import Session
from app.models.teaching import Student, Grade, Observation, ClassModel


def get_student_profile(db: Session, student_id: int) -> dict:
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise ValueError("学生不存在")

    grades = db.query(Grade).filter(Grade.student_id == student_id).order_by(Grade.id).all()

    # Knowledge point heatmap
    kp_scores = {}
    for g in grades:
        kp = g.knowledge_point or "未分类"
        if kp not in kp_scores:
            kp_scores[kp] = []
        kp_scores[kp].append(g.score)

    heatmap = []
    for kp, scores in kp_scores.items():
        avg = sum(scores) / len(scores)
        trend = "上升" if len(scores) >= 2 and scores[-1] > scores[0] else "下降" if len(scores) >= 2 and scores[-1] < scores[0] else "持平"
        heatmap.append({"knowledge_point": kp, "avg_score": round(avg, 1), "count": len(scores), "trend": trend})

    heatmap.sort(key=lambda x: x["avg_score"])
    weak = [h for h in heatmap if h["avg_score"] < 60][:3]
    strength = sorted(heatmap, key=lambda x: x["avg_score"], reverse=True)[:3]

    # Overall stats
    all_scores = [g.score for g in grades]
    avg = sum(all_scores) / len(all_scores) if all_scores else 0

    # Engagement score from observations
    cls = db.query(ClassModel).filter(ClassModel.id == student.class_id).first()
    obs_list = db.query(Observation).filter(Observation.class_id == student.class_id).all()
    engagement = sum(o.student_participation for o in obs_list) / len(obs_list) * 20 if obs_list else 50

    return {
        "student_id": student.id,
        "name": student.name,
        "student_no": student.student_no,
        "class_name": cls.name if cls else "",
        "avg_grade": round(avg, 1),
        "engagement_score": round(engagement, 1),
        "total_exams": len(grades),
        "heatmap": heatmap,
        "weak_points": weak,
        "strengths": strength,
        "recent_trend": [{"exam": g.exam_name, "score": g.score, "kp": g.knowledge_point} for g in grades[-6:]],
    }


def get_class_students_profile(db: Session, class_id: int) -> list[dict]:
    students = db.query(Student).filter(Student.class_id == class_id).all()
    return [get_student_profile(db, s.id) for s in students]
