from app.models.teaching import ClassModel
from app.schemas.teaching import ClassProfileResponse, ModeFingerprintResponse, DiagnosisResponse


def build_diagnosis(
    cls: ClassModel,
    profile: ClassProfileResponse,
    fingerprint: ModeFingerprintResponse,
) -> DiagnosisResponse:
    # Build teaching mode suggestion text
    dims = profile.dimensions
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
        parts.append(f"诊断发现该班级存在以下问题：{'；'.join(issues)}。")

    # Mode-based suggestions
    fp = fingerprint.fingerprint
    if fp.lecture_oriented > 0.6:
        parts.append("当前教学模式偏向讲授主导，建议引入更多互动和实践环节，如采用BOPPPS教学模式或翻转课堂。")
    elif fp.practice_oriented < 0.2:
        parts.append("实践环节占比较低，建议增加项目式学习(PBL)或案例分析教学，强化知识应用能力。")

    if profile.weak_points:
        weak_kps = [w.knowledge_point for w in profile.weak_points[:3]]
        parts.append(f"薄弱知识点集中在：{'、'.join(weak_kps)}，建议在这些知识点上采用具象化教学策略，配合靶向练习。")

    if not parts:
        parts.append("该班级整体学情良好，教学模式较为适配。建议继续保持现有教学策略，并定期通过平台追踪学情变化趋势。")

    suggestion = "".join(parts)

    return DiagnosisResponse(
        class_id=cls.id,
        class_name=cls.name,
        course_name=cls.course.name if cls.course else "",
        profile=profile,
        fingerprint=fingerprint,
        teaching_mode_suggestion=suggestion,
    )
