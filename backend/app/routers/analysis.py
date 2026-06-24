from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.teaching import ClassModel, Student, Grade, Observation, Evaluation
from app.schemas.teaching import (
    ClassProfileResponse, DimensionScores, KnowledgePoint,
    ModeFingerprintResponse, FingerprintScores, DiagnosisResponse,
)
from app.services.profile import compute_profile
from app.services.fingerprint import compute_fingerprint
from app.services.diagnosis import build_diagnosis


def get_class_profile(db: Session, class_id: int) -> ClassProfileResponse:
    cls = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if not cls:
        raise ValueError("班级不存在")

    return compute_profile(db, cls)


def get_mode_fingerprint(db: Session, class_id: int) -> ModeFingerprintResponse:
    cls = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if not cls:
        raise ValueError("班级不存在")

    return compute_fingerprint(db, cls)


def get_diagnosis(db: Session, class_id: int) -> DiagnosisResponse:
    cls = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if not cls:
        raise ValueError("班级不存在")

    profile = compute_profile(db, cls)
    fingerprint = compute_fingerprint(db, cls)
    return build_diagnosis(cls, profile, fingerprint)
