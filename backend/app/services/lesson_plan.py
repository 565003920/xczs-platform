"""Smart lesson plan generation — integrated with template library."""
from sqlalchemy.orm import Session
from app.models.teaching import ClassModel, Grade, Observation
from app.models.knowledge import KnowledgeNode, TeachingModeTemplate
from app.services.profile import compute_profile
from app.services.fingerprint import _match_template


def _get_class_mode_template(db: Session, class_id: int) -> TeachingModeTemplate | None:
    obs_list = db.query(Observation).filter(Observation.class_id == class_id).all()
    if not obs_list:
        return db.query(TeachingModeTemplate).filter(
            TeachingModeTemplate.category == "builtin",
            TeachingModeTemplate.name == "BOPPPS教学法"
        ).first()
    avg_lecture = sum(o.lecture_ratio for o in obs_list) / len(obs_list)
    avg_discussion = sum(o.discussion_ratio for o in obs_list) / len(obs_list)
    avg_practice = sum(o.practice_ratio for o in obs_list) / len(obs_list)
    if avg_lecture > 0.6: label = "讲授主导型"
    elif avg_discussion > 0.5: label = "互动讨论型"
    elif avg_practice > 0.4: label = "实践驱动型"
    else: label = "混合型(讲授+互动)"
    return _match_template(db, label, avg_lecture, avg_practice)


def generate_lesson_plan(db: Session, class_id: int, lesson_topic: str, duration: int = 50) -> dict:
    cls = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if not cls:
        raise ValueError("班级不存在")
    profile = compute_profile(db, cls)
    template = _get_class_mode_template(db, class_id)

    kps = db.query(KnowledgeNode).filter(
        KnowledgeNode.course_id == cls.course_id,
        KnowledgeNode.name.contains(lesson_topic)
    ).all()
    if not kps:
        kps = db.query(KnowledgeNode).filter(KnowledgeNode.course_id == cls.course_id).limit(3).all()

    key_points, quick_pass = [], []
    for kp in kps:
        grades = db.query(Grade).filter(Grade.knowledge_point == kp.name, Grade.class_id == class_id).all()
        avg = sum(g.score for g in grades) / len(grades) if grades else 50
        item = {"name": kp.name, "mastery": round(avg / 100, 2), "difficulty": kp.difficulty}
        (key_points if avg < 60 else quick_pass).append(item)

    # Build stages from template, scaled to duration
    if template and template.stages:
        template_stages = template.stages
        total = sum(s.get("duration", 10) for s in template_stages)
        scale = duration / total if total > 0 else 1
        stages, acc = [], 0
        for i, s in enumerate(template_stages):
            d = round(s.get("duration", 10) * scale)
            if i == len(template_stages) - 1: d = duration - acc
            acc += d
            stages.append({"name": s.get("name", f"环节{i+1}"), "duration": max(3, d),
                           "activity": s.get("teacher_action", "")})
    else:
        stages = [
            {"name": "导入", "duration": 5, "activity": "回顾前置知识"},
            {"name": "讲授", "duration": round(duration * 0.4), "activity": "系统讲解"},
            {"name": "练习", "duration": round(duration * 0.3), "activity": "课堂练习"},
            {"name": "总结", "duration": duration - 5 - round(duration * 0.4) - round(duration * 0.3), "activity": "总结要点"},
        ]

    tips = [
        f"📚 基于「{template.name if template else '通用'}」模板生成教学环节",
        f"📊 知识掌握度{profile.dimensions.knowledge_mastery*100:.0f}%，{'需加强基础巩固' if profile.dimensions.knowledge_mastery < 0.6 else '可适当提高难度'}",
        f"💬 参与度{profile.dimensions.participation*100:.0f}%，{'建议增加互动' if profile.dimensions.participation < 0.5 else '保持当前水平'}",
    ]
    if template and template.strengths:
        tips.append(f"✅ 该模式优势：{template.strengths}")

    return {
        "class_id": class_id, "class_name": cls.name,
        "course_name": cls.course.name if cls.course else "",
        "lesson_topic": lesson_topic, "duration": duration,
        "mode_template": template.name if template else "通用",
        "profile_summary": {"avg_grade": profile.avg_grade,
                            "knowledge_mastery": profile.dimensions.knowledge_mastery,
                            "participation": profile.dimensions.participation},
        "key_points": key_points, "quick_pass": quick_pass, "stages": stages, "tips": tips,
    }
