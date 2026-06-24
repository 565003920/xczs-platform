"""Smart lesson plan generation assistant."""
from sqlalchemy.orm import Session
from app.models.teaching import ClassModel, Grade, Observation, Evaluation
from app.models.knowledge import KnowledgeNode, TeachingModeTemplate
from app.services.profile import compute_profile


def generate_lesson_plan(db: Session, class_id: int, lesson_topic: str, duration: int = 50) -> dict:
    """Generate a teaching plan framework based on class profile."""
    cls = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if not cls:
        raise ValueError("班级不存在")

    profile = compute_profile(db, cls)

    # Find matching knowledge points
    kps = db.query(KnowledgeNode).filter(
        KnowledgeNode.course_id == cls.course_id,
        KnowledgeNode.name.contains(lesson_topic)
    ).all()
    if not kps:
        kps = db.query(KnowledgeNode).filter(KnowledgeNode.course_id == cls.course_id).limit(3).all()

    # Categorize points by mastery
    key_points = []
    quick_pass = []
    for kp in kps:
        grades = db.query(Grade).filter(Grade.knowledge_point == kp.name, Grade.class_id == class_id).all()
        avg = sum(g.score for g in grades) / len(grades) if grades else 50
        item = {"name": kp.name, "mastery": round(avg / 100, 2), "difficulty": kp.difficulty}
        if avg < 60:
            key_points.append(item)
        else:
            quick_pass.append(item)

    # Recommend stages
    obs_list = db.query(Observation).filter(Observation.class_id == class_id).all()
    is_lecture_heavy = sum(o.lecture_ratio for o in obs_list) / len(obs_list) > 0.6 if obs_list else False

    if is_lecture_heavy:
        stages = [
            {"name": "导入", "duration": 5, "activity": "情境导入，激发兴趣"},
            {"name": "互动讲授", "duration": round(duration * 0.3), "activity": "精讲核心概念，穿插提问"},
            {"name": "小组讨论", "duration": round(duration * 0.25), "activity": "围绕重难点分组讨论"},
            {"name": "练习巩固", "duration": round(duration * 0.25), "activity": "典型例题 + 变式练习"},
            {"name": "总结提升", "duration": duration - 5 - round(duration * 0.3) - round(duration * 0.25) - round(duration * 0.25), "activity": "归纳总结，布置作业"},
        ]
    else:
        stages = [
            {"name": "导入复习", "duration": 5, "activity": "回顾前置知识"},
            {"name": "新知讲授", "duration": round(duration * 0.4), "activity": "系统讲解新内容"},
            {"name": "案例分析", "duration": round(duration * 0.25), "activity": "结合案例深化理解"},
            {"name": "互动练习", "duration": round(duration * 0.2), "activity": "课堂练习 + 即时反馈"},
            {"name": "总结", "duration": duration - 5 - round(duration * 0.4) - round(duration * 0.25) - round(duration * 0.2), "activity": "总结要点"},
        ]

    return {
        "class_id": class_id,
        "class_name": cls.name,
        "course_name": cls.course.name if cls.course else "",
        "lesson_topic": lesson_topic,
        "duration": duration,
        "profile_summary": {
            "avg_grade": profile.avg_grade,
            "knowledge_mastery": profile.dimensions.knowledge_mastery,
            "participation": profile.dimensions.participation,
        },
        "key_points": key_points,
        "quick_pass": quick_pass,
        "stages": stages,
        "tips": [
            f"班级知识掌握度为{profile.dimensions.knowledge_mastery*100:.0f}%，{'需要加强基础巩固' if profile.dimensions.knowledge_mastery < 0.6 else '可适当提高难度'}",
            f"课堂参与度{profile.dimensions.participation*100:.0f}%，{'建议增加互动环节' if profile.dimensions.participation < 0.5 else '保持当前互动水平'}",
        ],
    }
