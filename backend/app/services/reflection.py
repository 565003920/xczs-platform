"""Post-class reflection assistant."""
from sqlalchemy.orm import Session
from app.models.teaching import ClassModel, Observation, Grade, Evaluation


def generate_reflection(db: Session, class_id: int, observation_id: int = None) -> dict:
    """Generate a post-class reflection report."""
    cls = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if not cls:
        raise ValueError("班级不存在")

    # Get latest observation
    obs = None
    if observation_id:
        obs = db.query(Observation).filter(Observation.id == observation_id).first()
    if not obs:
        obs = db.query(Observation).filter(Observation.class_id == class_id).order_by(Observation.id.desc()).first()

    if not obs:
        return {"class_id": class_id, "note": "暂无课堂观察数据"}

    # Compute achievement estimation
    grades = db.query(Grade).filter(Grade.class_id == class_id).all()
    recent = grades[-10:] if len(grades) > 10 else grades
    avg_recent = sum(g.score for g in recent) / len(recent) if recent else 0

    # Analyze deviation from expected mode
    all_obs = db.query(Observation).filter(Observation.class_id == class_id).all()
    avg_lecture = sum(o.lecture_ratio for o in all_obs) / len(all_obs) if all_obs else 0.5
    avg_discussion = sum(o.discussion_ratio for o in all_obs) / len(all_obs) if all_obs else 0.3

    deviations = []
    if avg_lecture > 0.6:
        deviations.append({"aspect": "讲授占比偏高", "current": f"{avg_lecture*100:.0f}%", "ideal": "40-50%", "suggestion": "减少讲授时间，增加学生活动"})
    if avg_discussion < 0.2:
        deviations.append({"aspect": "讨论互动不足", "current": f"{avg_discussion*100:.0f}%", "ideal": "20-30%", "suggestion": "增加小组讨论或同伴互评环节"})

    # Satisfaction
    ev = db.query(Evaluation).filter(Evaluation.class_id == class_id, Evaluation.dimension == "overall_satisfaction").first()
    satisfaction = ev.score if ev else 0

    suggestions = []
    if avg_lecture > 0.6:
        suggestions.append("尝试将部分讲授内容转为课前视频，课堂时间用于深度互动")
    if obs.student_participation < 3:
        suggestions.append("下次课增加课堂即时投票或小组竞赛提升参与度")
    if avg_recent < 60:
        suggestions.append("考虑放慢教学节奏，增设课后辅导环节")
    if not suggestions:
        suggestions.append("当前教学节奏良好，继续保持并追踪学情变化")

    return {
        "class_id": class_id,
        "class_name": cls.name,
        "observation_date": obs.date,
        "mode_label": obs.teaching_style_label or "未标注",
        "achievement_estimation": {
            "recent_avg_grade": round(avg_recent, 1),
            "level": "优秀" if avg_recent >= 85 else "良好" if avg_recent >= 70 else "一般" if avg_recent >= 60 else "需关注",
        },
        "observation_summary": {
            "interaction": f"{obs.interaction_frequency}/5",
            "question_depth": f"{obs.question_depth}/5",
            "participation": f"{obs.student_participation}/5",
        },
        "deviations": deviations,
        "satisfaction": round(satisfaction / 100, 2) if satisfaction > 1 else round(satisfaction, 2),
        "improvement_suggestions": suggestions,
    }
