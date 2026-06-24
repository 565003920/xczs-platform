"""Diagnosis report — integrated with template library + optional LLM enhancement."""
from app.models.teaching import ClassModel
from app.schemas.teaching import ClassProfileResponse, ModeFingerprintResponse, DiagnosisResponse
from app.services.llm import call_llm


def build_diagnosis(cls: ClassModel, profile: ClassProfileResponse,
                    fingerprint: ModeFingerprintResponse) -> DiagnosisResponse:
    dims = profile.dimensions
    fp = fingerprint.fingerprint
    parts = []

    # Analyze weak areas
    issues = []
    if dims.knowledge_mastery < 0.6:
        issues.append(f"知识掌握度偏低({dims.knowledge_mastery*100:.0f}%)")
    if dims.participation < 0.5:
        issues.append(f"课堂参与度不足({dims.participation*100:.0f}%)")
    if dims.question_depth < 0.5:
        issues.append(f"提问层次偏低({dims.question_depth*100:.0f}%)")
    if issues:
        parts.append(f"诊断发现：{'；'.join(issues)}。")

    if fp.lecture_oriented > 0.6:
        parts.append("当前模式偏向讲授主导，建议引入「翻转课堂」或「对分课堂」，将部分内容移至课前或交互环节。")
    elif fp.practice_oriented < 0.2:
        parts.append("实践环节占比较低，建议参考「PBL项目式学习」或「探究式学习」模板，增加动手实践。")

    for rec in fingerprint.mode_recommendations[:2]:
        if rec not in "".join(parts):
            parts.append(rec)

    if profile.weak_points:
        weak_kps = [w.knowledge_point for w in profile.weak_points[:3]]
        parts.append(f"薄弱知识点：{'、'.join(weak_kps)}，建议在这些知识点采用具象化教学策略，配合靶向练习。")

    if not parts:
        parts.append("该班级整体学情良好，当前教学模式较为适配。建议继续保持，并定期通过平台追踪学情变化趋势。")

    base_text = "".join(parts)

    # ── LLM enhancement ──
    llm_text = call_llm(
        system_prompt="你是一位资深教育专家。请将以下教学诊断数据整合为一段200字以内的综合诊断建议。保持专业、具体、可操作。直接输出建议文本，不要加前缀。",
        user_prompt=f"""班级：{cls.name}，课程：{cls.course.name if cls.course else ''}
平均成绩：{profile.avg_grade}分，知识掌握度：{profile.dimensions.knowledge_mastery*100:.0f}%
参与度：{profile.dimensions.participation*100:.0f}%，满意度：{profile.dimensions.satisfaction*100:.0f}%
当前模式：{fingerprint.mode_label}
原始诊断：{base_text}""",
        max_tokens=300,
    )

    return DiagnosisResponse(
        class_id=cls.id, class_name=cls.name,
        course_name=cls.course.name if cls.course else "",
        teacher_name=cls.course.teacher_name if cls.course else "",
        profile=profile, fingerprint=fingerprint,
        teaching_mode_suggestion=llm_text or base_text,
    )
