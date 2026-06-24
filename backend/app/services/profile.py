from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import Counter
from app.models.teaching import ClassModel, Student, Grade, Observation, Evaluation
from app.schemas.teaching import ClassProfileResponse, DimensionScores, KnowledgePoint


def compute_profile(db: Session, cls: ClassModel) -> ClassProfileResponse:
    # --- Grade stats ---
    grades = db.query(Grade).filter(Grade.class_id == cls.id).all()
    total_grades = len(grades)
    avg_grade = sum(g.score for g in grades) / total_grades if total_grades > 0 else 0.0

    # Grade distribution
    dist = {"90-100": 0, "80-89": 0, "70-79": 0, "60-69": 0, "0-59": 0}
    for g in grades:
        s = g.score
        if s >= 90:
            dist["90-100"] += 1
        elif s >= 80:
            dist["80-89"] += 1
        elif s >= 70:
            dist["70-79"] += 1
        elif s >= 60:
            dist["60-69"] += 1
        else:
            dist["0-59"] += 1

    # Knowledge points
    kp_map = {}
    for g in grades:
        kp = g.knowledge_point or "未分类"
        if kp not in kp_map:
            kp_map[kp] = []
        kp_map[kp].append(g.score)
    kp_items = []
    for kp, scores in kp_map.items():
        kp_items.append(KnowledgePoint(knowledge_point=kp, avg_score=round(sum(scores) / len(scores), 1)))
    kp_items.sort(key=lambda x: x.avg_score)
    weak_points = kp_items[:5]
    strengths = sorted(kp_items, key=lambda x: x.avg_score, reverse=True)[:5]

    # --- Observations ---
    obs_list = db.query(Observation).filter(Observation.class_id == cls.id).all()
    obs_n = len(obs_list)
    if obs_n > 0:
        avg_interaction = sum(o.interaction_frequency for o in obs_list) / obs_n
        avg_question = sum(o.question_depth for o in obs_list) / obs_n
        avg_participation = sum(o.student_participation for o in obs_list) / obs_n
        avg_lecture = sum(o.lecture_ratio for o in obs_list) / obs_n
        avg_discussion = sum(o.discussion_ratio for o in obs_list) / obs_n
        avg_practice = sum(o.practice_ratio for o in obs_list) / obs_n
    else:
        avg_interaction = avg_question = avg_participation = 3.0
        avg_lecture, avg_discussion, avg_practice = 0.5, 0.3, 0.2

    # Practice balance: ideal is ~0.3 practice, deviation penalty
    ideal_practice = 0.3
    practice_balance = max(0.0, 1.0 - abs(ideal_practice - avg_practice) * 2)

    # --- Evaluations ---
    evals = db.query(Evaluation).filter(Evaluation.class_id == cls.id).all()
    satisfaction = 0.0
    for e in evals:
        if e.dimension == "overall_satisfaction":
            satisfaction = e.score / 100.0 if e.score > 1 else e.score
            break

    dimensions = DimensionScores(
        knowledge_mastery=round(min(avg_grade / 100.0, 1.0), 2),
        participation=round(min(avg_participation / 5.0, 1.0), 2),
        interaction_quality=round(min(avg_interaction / 5.0, 1.0), 2),
        question_depth=round(min(avg_question / 5.0, 1.0), 2),
        practice_balance=round(practice_balance, 2),
        satisfaction=round(satisfaction, 2),
    )

    return ClassProfileResponse(
        class_id=cls.id,
        class_name=cls.name,
        course_name=cls.course.name if cls.course else "",
        teacher_name=cls.course.teacher_name if cls.course else "",
        dimensions=dimensions,
        weak_points=weak_points,
        strengths=strengths,
        student_count=db.query(Student).filter(Student.class_id == cls.id).count(),
        avg_grade=round(avg_grade, 1),
        grade_distribution=dist,
    )
