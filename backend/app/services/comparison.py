"""Effect size computation and A/B comparison for teaching modes."""
import math
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.teaching import ClassModel, Grade, Observation, Evaluation
from app.schemas.teaching import (
    DimensionScores, ClassProfileResponse,
    FingerprintScores, ModeFingerprintResponse,
)


def cohens_d(group_a: list[float], group_b: list[float]) -> float:
    """Compute Cohen's d effect size between two groups."""
    n_a, n_b = len(group_a), len(group_b)
    if n_a < 2 or n_b < 2:
        return 0.0
    mean_a = sum(group_a) / n_a
    mean_b = sum(group_b) / n_b
    var_a = sum((x - mean_a) ** 2 for x in group_a) / (n_a - 1)
    var_b = sum((x - mean_b) ** 2 for x in group_b) / (n_b - 1)
    pooled_sd = math.sqrt(((n_a - 1) * var_a + (n_b - 1) * var_b) / (n_a + n_b - 2))
    if pooled_sd == 0:
        return 0.0
    return (mean_a - mean_b) / pooled_sd


def interpret_effect(d: float) -> str:
    d_abs = abs(d)
    if d_abs < 0.2:
        return "效应很小（可忽略）"
    elif d_abs < 0.5:
        return "效应较小"
    elif d_abs < 0.8:
        return "效应中等"
    else:
        return "效应显著"


def compare_modes(db: Session, class_id_a: int, class_id_b: int) -> dict:
    """Compare two classes' teaching effectiveness."""
    cls_a = db.query(ClassModel).filter(ClassModel.id == class_id_a).first()
    cls_b = db.query(ClassModel).filter(ClassModel.id == class_id_b).first()
    if not cls_a or not cls_b:
        raise ValueError("班级不存在")

    # Grades comparison
    grades_a = [g.score for g in db.query(Grade).filter(Grade.class_id == class_id_a).all()]
    grades_b = [g.score for g in db.query(Grade).filter(Grade.class_id == class_id_b).all()]
    d_grade = cohens_d(grades_a, grades_b)
    mean_a = sum(grades_a) / len(grades_a) if grades_a else 0
    mean_b = sum(grades_b) / len(grades_b) if grades_b else 0

    # Observations
    obs_a = db.query(Observation).filter(Observation.class_id == class_id_a).all()
    obs_b = db.query(Observation).filter(Observation.class_id == class_id_b).all()

    def avg_obs(obs_list, attr):
        vals = [getattr(o, attr) for o in obs_list]
        return sum(vals) / len(vals) if vals else 0

    # Satisfaction from evaluations
    def get_satisfaction(class_id):
        ev = db.query(Evaluation).filter(
            Evaluation.class_id == class_id,
            Evaluation.dimension == "overall_satisfaction"
        ).first()
        return ev.score / 100.0 if ev and ev.score > 1 else (ev.score if ev else 0)

    sat_a = get_satisfaction(class_id_a)
    sat_b = get_satisfaction(class_id_b)

    effect_grade = interpret_effect(d_grade)

    return {
        "class_a": {"id": cls_a.id, "name": cls_a.name, "course_name": cls_a.course.name if cls_a.course else ""},
        "class_b": {"id": cls_b.id, "name": cls_b.name, "course_name": cls_b.course.name if cls_b.course else ""},
        "grade_comparison": {
            "mean_a": round(mean_a, 1),
            "mean_b": round(mean_b, 1),
            "difference": round(mean_a - mean_b, 1),
            "cohens_d": round(d_grade, 3),
            "interpretation": effect_grade,
            "sample_size_a": len(grades_a),
            "sample_size_b": len(grades_b),
        },
        "dimension_comparison": {
            "interaction_quality": {"a": round(avg_obs(obs_a, "interaction_frequency") / 5, 2), "b": round(avg_obs(obs_b, "interaction_frequency") / 5, 2)},
            "question_depth": {"a": round(avg_obs(obs_a, "question_depth") / 5, 2), "b": round(avg_obs(obs_b, "question_depth") / 5, 2)},
            "participation": {"a": round(avg_obs(obs_a, "student_participation") / 5, 2), "b": round(avg_obs(obs_b, "student_participation") / 5, 2)},
            "lecture_ratio": {"a": round(avg_obs(obs_a, "lecture_ratio"), 2), "b": round(avg_obs(obs_b, "lecture_ratio"), 2)},
            "practice_ratio": {"a": round(avg_obs(obs_a, "practice_ratio"), 2), "b": round(avg_obs(obs_b, "practice_ratio"), 2)},
            "satisfaction": {"a": round(sat_a, 2), "b": round(sat_b, 2)},
        },
    }


def cross_teacher_compare(db: Session, course_id: int) -> dict:
    """Compare all classes under a course, ranked by performance."""
    classes = db.query(ClassModel).filter(ClassModel.course_id == course_id).all()
    if len(classes) < 2:
        return {"course_id": course_id, "rankings": [], "note": "需要至少2个班级才能对比"}

    rankings = []
    for cls in classes:
        grades = [g.score for g in db.query(Grade).filter(Grade.class_id == cls.id).all()]
        avg_g = sum(grades) / len(grades) if grades else 0
        obs_list = db.query(Observation).filter(Observation.class_id == cls.id).all()
        avg_participation = sum(o.student_participation for o in obs_list) / len(obs_list) if obs_list else 0
        ev = db.query(Evaluation).filter(
            Evaluation.class_id == cls.id,
            Evaluation.dimension == "overall_satisfaction"
        ).first()
        sat = ev.score / 100.0 if ev and ev.score > 1 else (ev.score if ev else 0)

        rankings.append({
            "class_id": cls.id,
            "class_name": cls.name,
            "avg_grade": round(avg_g, 1),
            "avg_participation": round(avg_participation, 1),
            "satisfaction": round(sat, 2),
        })

    rankings.sort(key=lambda x: x["avg_grade"], reverse=True)
    return {"course_id": course_id, "course_name": classes[0].course.name if classes[0].course else "", "rankings": rankings}


def teacher_trend(db: Session, course_id: int) -> dict:
    """Get semester-by-semester trend for a course."""
    classes = db.query(ClassModel).filter(
        ClassModel.course_id == course_id
    ).order_by(ClassModel.semester_index, ClassModel.id).all()

    if not classes:
        return {"course_id": course_id, "semesters": []}

    semesters = []
    for cls in classes:
        grades = [g.score for g in db.query(Grade).filter(Grade.class_id == cls.id).all()]
        avg_g = sum(grades) / len(grades) if grades else 0
        obs_list = db.query(Observation).filter(Observation.class_id == cls.id).all()
        mode_label = obs_list[0].teaching_style_label if obs_list else "未知"
        ev = db.query(Evaluation).filter(
            Evaluation.class_id == cls.id,
            Evaluation.dimension == "overall_satisfaction"
        ).first()
        sat = ev.score / 100.0 if ev and ev.score > 1 else (ev.score if ev else 0)

        semesters.append({
            "class_id": cls.id,
            "class_name": cls.name,
            "semester": cls.semester,
            "semester_index": cls.semester_index,
            "avg_grade": round(avg_g, 1),
            "satisfaction": round(sat, 2),
            "mode_label": mode_label,
        })

    return {
        "course_id": course_id,
        "course_name": classes[0].course.name if classes[0].course else "",
        "semesters": semesters,
    }
