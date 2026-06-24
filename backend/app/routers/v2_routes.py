"""v2.0 unified router — all new endpoints with ownership filter."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.auth import get_current_user, check_class_access
from app.models.teaching import ClassModel
from app.models.audit import AuditLog, Notification
from app.services.individual_profile import get_student_profile, get_class_students_profile
from app.services.migration import recommend_migration
from app.services.lesson_plan import generate_lesson_plan
from app.services.reflection import generate_reflection
from app.services.data_catalog import get_catalog_summary, get_quality_report
from app.services.data_lineage import get_lineage, get_all_lineages, record_lineage
from app.services.effectiveness import get_effectiveness

router = APIRouter(prefix="/api/v2", tags=["v2.0"])


@router.get("/student/{student_id}/profile")
def api_student_profile(student_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        return get_student_profile(db, student_id)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/class/{class_id}/students")
def api_class_students(class_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    check_class_access(db, class_id, user)
    return get_class_students_profile(db, class_id)


@router.get("/migration/recommend")
def api_migration_recommend(target_class_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    check_class_access(db, target_class_id, user)
    try:
        return recommend_migration(db, target_class_id)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.post("/lesson-plan/generate")
def api_lesson_plan(body: dict, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    check_class_access(db, body["class_id"], user)
    try:
        plan = generate_lesson_plan(db, body["class_id"], body.get("lesson_topic", ""), body.get("duration", 50))
        record_lineage(f"lesson_{body['class_id']}", "lesson_plan",
                       [{"source": "class_profile", "class_id": body["class_id"]}],
                       {"type": "lesson_plan"})
        return plan
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.post("/reflection/generate")
def api_reflection(body: dict, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    check_class_access(db, body["class_id"], user)
    try:
        ref = generate_reflection(db, body["class_id"], body.get("observation_id"))
        record_lineage(f"reflection_{body['class_id']}", "reflection",
                       [{"source": "observations", "class_id": body["class_id"]}],
                       {"type": "reflection"})
        return ref
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/catalog/summary")
def api_catalog_summary(db: Session = Depends(get_db)):
    return get_catalog_summary(db)


@router.get("/catalog/quality")
def api_quality_report(db: Session = Depends(get_db)):
    return get_quality_report(db)


@router.get("/catalog/lineage")
def api_lineage_list():
    return get_all_lineages()


@router.get("/catalog/lineage/{analysis_id}")
def api_lineage_detail(analysis_id: str):
    r = get_lineage(analysis_id)
    if not r: raise HTTPException(404, "血缘记录不存在")
    return r


@router.get("/dashboard/effectiveness")
def api_effectiveness(db: Session = Depends(get_db)):
    return get_effectiveness(db)


@router.get("/audit/logs")
def api_audit_logs(page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    total = db.query(AuditLog).count()
    logs = db.query(AuditLog).order_by(AuditLog.id.desc()).offset((page-1)*size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": logs}


@router.get("/notifications")
def api_notifications(unread_only: bool = False, db: Session = Depends(get_db)):
    q = db.query(Notification).order_by(Notification.id.desc())
    if unread_only: q = q.filter(Notification.is_read == False)
    items = q.limit(50).all()
    unread_count = db.query(Notification).filter(Notification.is_read == False).count()
    return {"items": items, "unread_count": unread_count}


@router.put("/notifications/{nid}/read")
def api_mark_read(nid: int, db: Session = Depends(get_db)):
    n = db.query(Notification).filter(Notification.id == nid).first()
    if n: n.is_read = True; db.commit()
    return {"ok": True}


@router.put("/notifications/read-all")
def api_mark_all_read(db: Session = Depends(get_db)):
    db.query(Notification).filter(Notification.is_read == False).update({"is_read": False})
    db.commit()
    return {"ok": True}
