"""Effectiveness dashboard service."""
from sqlalchemy.orm import Session
from app.models.teaching import Course, ClassModel, Student, Grade
from app.models.knowledge import TeachingModeTemplate
from app.services.data_catalog import get_catalog_summary


def get_effectiveness(db: Session) -> dict:
    catalog = get_catalog_summary(db)

    total_courses = db.query(Course).count()
    total_classes = db.query(ClassModel).count()
    total_students = db.query(Student).count()
    total_grades = db.query(Grade).count()

    # Average grade across all
    all_grades = db.query(Grade).all()
    avg_all = sum(g.score for g in all_grades) / len(all_grades) if all_grades else 0

    # Mode usage
    modes = db.query(TeachingModeTemplate).all()
    top_modes = sorted(modes, key=lambda m: m.usage_count or 0, reverse=True)[:5]
    top_mode_list = [{"name": m.name, "usage": m.usage_count or 0} for m in top_modes]

    # Distribution stats
    dist = {"90-100": 0, "80-89": 0, "70-79": 0, "60-69": 0, "0-59": 0}
    for g in all_grades:
        s = g.score
        if s >= 90: dist["90-100"] += 1
        elif s >= 80: dist["80-89"] += 1
        elif s >= 70: dist["70-79"] += 1
        elif s >= 60: dist["60-69"] += 1
        else: dist["0-59"] += 1

    return {
        "summary": {
            "total_courses": total_courses,
            "total_classes": total_classes,
            "total_students": total_students,
            "total_grades": total_grades,
            "avg_grade": round(avg_all, 1),
            "data_assets": catalog["total_records"],
        },
        "top_modes": top_mode_list,
        "grade_distribution": dist,
        "data_quality": {
            "overall": round(sum(a["quality_score"] for a in catalog["assets"]) / max(len(catalog["assets"]), 1)),
            "details": catalog["assets"],
        },
    }
