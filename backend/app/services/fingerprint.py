from sqlalchemy.orm import Session
from app.models.teaching import ClassModel, Observation
from app.schemas.teaching import ModeFingerprintResponse, FingerprintScores


def _determine_mode_label(lecture: float, discussion: float, practice: float) -> str:
    if lecture > 0.6:
        return "讲授主导型"
    elif discussion > 0.5:
        return "互动讨论型"
    elif practice > 0.4:
        return "实践驱动型"
    else:
        return "混合型(讲授+互动)"


def _generate_description(label: str, lecture: float, discussion: float, practice: float, question: float, participation: float) -> str:
    parts = [f"该班级教学以讲授为主({lecture*100:.0f}%)" if lecture > 0.4 else ""]
    if discussion > 0.2:
        parts.append(f"辅以课堂互动({discussion*100:.0f}%)")
    if practice > 0.15:
        parts.append(f"和实践环节({practice*100:.0f}%)")
    desc = "，".join([p for p in parts if p])
    desc += "。"
    if question >= 4:
        desc += "提问层次较高，注重启发式教学。"
    elif question >= 3:
        desc += "提问以理解型为主。"
    else:
        desc += "提问偏向记忆型。"
    if participation >= 4:
        desc += "学生参与度较高。"
    elif participation >= 3:
        desc += "学生参与度中等偏上。"
    else:
        desc += "学生参与度有待提升。"
    return desc


def _generate_recommendations(label: str, lecture: float, practice: float, question: float, participation: float) -> list[str]:
    recs = []
    if practice < 0.25:
        recs.append("建议增加PBL项目式学习环节以提升实践比重")
    if lecture > 0.6:
        recs.append("可尝试对分课堂模式增强学生自主学习")
    if participation < 3.5:
        recs.append("引入小组讨论和同伴互评提升学生参与度")
    if question < 3.5:
        recs.append("增加高阶思维提问（分析、评价、创造层次）")
    if label == "讲授主导型":
        recs.append("逐步引入翻转课堂，将部分内容移至课前自学")
    return recs if recs else ["当前教学模式较为均衡，可继续保持并精细化数据追踪"]


def compute_fingerprint(db: Session, cls: ClassModel) -> ModeFingerprintResponse:
    obs_list = db.query(Observation).filter(Observation.class_id == cls.id).all()
    obs_n = len(obs_list)

    if obs_n == 0:
        return ModeFingerprintResponse(
            class_id=cls.id,
            fingerprint=FingerprintScores(),
            mode_label="数据不足",
            mode_description="暂无足够的课堂观察数据",
            mode_recommendations=["请先录入课堂观察数据"],
            observation_count=0,
        )

    avg_lecture = sum(o.lecture_ratio for o in obs_list) / obs_n
    avg_discussion = sum(o.discussion_ratio for o in obs_list) / obs_n
    avg_practice = sum(o.practice_ratio for o in obs_list) / obs_n
    avg_question = sum(o.question_depth for o in obs_list) / obs_n / 5.0
    avg_participation = sum(o.student_participation for o in obs_list) / obs_n / 5.0

    label = _determine_mode_label(avg_lecture, avg_discussion, avg_practice)
    desc = _generate_description(label, avg_lecture, avg_discussion, avg_practice, avg_question * 5, avg_participation * 5)
    recs = _generate_recommendations(label, avg_lecture, avg_practice, avg_question * 5, avg_participation * 5)

    return ModeFingerprintResponse(
        class_id=cls.id,
        fingerprint=FingerprintScores(
            lecture_oriented=round(avg_lecture, 2),
            interactive=round(avg_discussion, 2),
            practice_oriented=round(avg_practice, 2),
            question_level=round(avg_question, 2),
            student_centeredness=round(avg_participation, 2),
        ),
        mode_label=label,
        mode_description=desc,
        mode_recommendations=recs,
        observation_count=obs_n,
    )
