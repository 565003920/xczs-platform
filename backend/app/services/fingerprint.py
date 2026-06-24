"""Teaching mode fingerprint — integrated with template library + optional LLM."""
from sqlalchemy.orm import Session
from app.models.teaching import ClassModel, Observation
from app.models.knowledge import TeachingModeTemplate
from app.schemas.teaching import ModeFingerprintResponse, FingerprintScores
from app.services.llm import call_llm


_LABEL_TO_TEMPLATE = {
    "讲授主导型": ["讲授+练习式", "翻转课堂"],
    "互动讨论型": ["对分课堂", "同伴教学法", "研讨式教学"],
    "实践驱动型": ["PBL项目式学习", "探究式学习"],
    "混合型(讲授+互动)": ["BOPPPS教学法", "混合式教学", "案例教学法", "5E教学法", "游戏化教学"],
}


def _match_template(db: Session, label: str, lecture: float, practice: float) -> TeachingModeTemplate | None:
    """Find the best-matching template from the library."""
    candidates = _LABEL_TO_TEMPLATE.get(label, [])
    templates = db.query(TeachingModeTemplate).filter(
        TeachingModeTemplate.category == "builtin",
        TeachingModeTemplate.name.in_(candidates)
    ).all()
    if templates:
        # Prefer practice-oriented if practice ratio is high
        if practice > 0.35:
            for t in templates:
                if "实践" in t.suitable_scenarios or "项目" in t.name:
                    return t
        return templates[0]
    # Fallback: fuzzy search by keyword
    keywords = label.replace("型", "").replace("(", "").replace(")", "")
    all_builtin = db.query(TeachingModeTemplate).filter(TeachingModeTemplate.category == "builtin").all()
    for t in all_builtin:
        if any(kw in t.name for kw in keywords.split("+")):
            return t
    return None


def _generate_recommendations(label: str, template: TeachingModeTemplate | None,
                               lecture: float, practice: float, question: float, participation: float) -> list[str]:
    """Generate recommendations, enriched by template library."""
    recs = []

    # Data-driven suggestions
    if practice < 0.25:
        recs.append("建议增加PBL项目式学习环节以提升实践比重")
    if lecture > 0.6:
        recs.append("可尝试对分课堂模式增强学生自主学习")
    if participation < 3.5:
        recs.append("引入小组讨论和同伴互评提升学生参与度")
    if question < 3.5:
        recs.append("增加高阶思维提问（分析、评价、创造层次）")

    # Template-aware suggestions
    if template:
        if template.limitations:
            recs.append(f"当前模式注意点：{template.limitations}")
        # Suggest complementary templates
        if "讲授" in label and "翻转" not in " ".join(recs):
            recs.append("逐步引入翻转课堂，将部分内容移至课前自学")
        if "互动" in label and "PBL" not in " ".join(recs):
            recs.append("可升级为PBL项目式学习，增强真实场景应用")

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

    # Determine hard label, then match to template library
    if avg_lecture > 0.6:
        label = "讲授主导型"
    elif avg_discussion > 0.5:
        label = "互动讨论型"
    elif avg_practice > 0.4:
        label = "实践驱动型"
    else:
        label = "混合型(讲授+互动)"

    template = _match_template(db, label, avg_lecture, avg_practice)

    # Build description: use template's if available, else generate
    if template:
        desc = f"识别为「{template.name}」模式。{template.description or ''} "
        desc += f"| 数据特征：讲授{avg_lecture*100:.0f}% 互动{avg_discussion*100:.0f}% 实践{avg_practice*100:.0f}%。"
        if template.strengths:
            desc += f"优势：{template.strengths}。"
    else:
        parts = [f"该班级教学以讲授为主({avg_lecture*100:.0f}%)" if avg_lecture > 0.4 else ""]
        if avg_discussion > 0.2:
            parts.append(f"辅以课堂互动({avg_discussion*100:.0f}%)")
        if avg_practice > 0.15:
            parts.append(f"和实践环节({avg_practice*100:.0f}%)")
        desc = "，".join([p for p in parts if p]) + "。"
        if avg_question * 5 >= 4:
            desc += "提问层次较高。"
        elif avg_question * 5 >= 3:
            desc += "提问以理解型为主。"
        else:
            desc += "提问偏向记忆型。"
        if avg_participation * 5 >= 4:
            desc += "学生参与度较高。"
        elif avg_participation * 5 >= 3:
            desc += "学生参与度中等偏上。"
        else:
            desc += "学生参与度有待提升。"

    recs = _generate_recommendations(label, template, avg_lecture, avg_practice, avg_question * 5, avg_participation * 5)

    # ── LLM enhancement ──
    if template:
        llm_desc = call_llm(
            system_prompt="你是一位教学诊断专家。请根据课堂教学数据生成一段80字以内的教学模式描述，包含模式名称、数据特征和优势。直接输出，不要前缀。",
            user_prompt=f"模式：{template.name}，讲授{avg_lecture*100:.0f}% 互动{avg_discussion*100:.0f}% 实践{avg_practice*100:.0f}%，提问层次{avg_question*5:.0f}/5，学生参与度{avg_participation*5:.0f}/5。模板描述：{template.description or ''}。优势：{template.strengths or ''}",
            max_tokens=150,
        )
        if llm_desc:
            desc = llm_desc

        llm_recs = call_llm(
            system_prompt="你是一位教学改进顾问。请根据教学模式数据生成2条具体的改进建议，每条20字以内。直接输出，用换行分隔。",
            user_prompt=f"讲授{avg_lecture*100:.0f}% 实践{avg_practice*100:.0f}% 参与度{avg_participation*5:.0f}/5。模式：{template.name}。局限：{template.limitations or ''}。已有建议：{'；'.join(recs[:2])}",
            max_tokens=100,
        )
        if llm_recs:
            new_recs = [r.strip() for r in llm_recs.strip().split("\n") if r.strip()]
            if new_recs:
                recs = new_recs + recs

    return ModeFingerprintResponse(
        class_id=cls.id,
        fingerprint=FingerprintScores(
            lecture_oriented=round(avg_lecture, 2),
            interactive=round(avg_discussion, 2),
            practice_oriented=round(avg_practice, 2),
            question_level=round(avg_question, 2),
            student_centeredness=round(avg_participation, 2),
        ),
        mode_label=template.name if template else label,
        mode_description=desc,
        mode_recommendations=recs,
        observation_count=obs_n,
    )
