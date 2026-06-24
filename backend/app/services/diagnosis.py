"""Diagnosis report — integrated with template library."""
from app.models.teaching import ClassModel
from app.schemas.teaching import ClassProfileResponse, ModeFingerprintResponse, DiagnosisResponse


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

    # Mode-based suggestions
    if fp.lecture_oriented > 0.6:
        parts.append("当前模式偏向讲授主导，建议引入「翻转课堂」或「对分课堂」，将部分内容移至课前或交互环节。")
    elif fp.practice_oriented < 0.2:
        parts.append("实践环节占比较低，建议参考「PBL项目式学习」或「探究式学习」模板，增加动手实践。")

    # Reference template suggestions from fingerprint
    for rec in fingerprint.mode_recommendations[:2]:
        if rec not in "".join(parts):
            parts.append(rec)

    # Knowledge point weaknesses
    if profile.weak_points:
        weak_kps = [w.knowledge_point for w in profile.weak_points[:3]]
        parts.append(f"薄弱知识点：{'、'.join(weak_kps)}，建议在这些知识点采用具象化教学策略，配合靶向练习。")

    if not parts:
        parts.append("该班级整体学情良好，当前教学模式较为适配。建议继续保持，并定期通过平台追踪学情变化趋势。")

    return DiagnosisResponse(
        class_id=cls.id,
        class_name=cls.name,
        course_name=cls.course.name if cls.course else "",
        profile=profile,
        fingerprint=fingerprint,
        teaching_mode_suggestion="".join(parts),
    )
