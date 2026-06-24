from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.auth import get_current_user, check_class_access
from app.services.comparison import compare_modes, cross_teacher_compare, teacher_trend

router = APIRouter(prefix="/api/analysis", tags=["comparison"])


@router.get("/compare/modes")
def api_compare_modes(class_a: int, class_b: int, db: Session = Depends(get_db),
                      user: dict = Depends(get_current_user)):
    check_class_access(db, class_a, user)
    check_class_access(db, class_b, user)
    try:
        return compare_modes(db, class_a, class_b)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/compare/cross-teacher")
def api_cross_teacher(course_id: int, db: Session = Depends(get_db),
                      user: dict = Depends(get_current_user)):
    try:
        return cross_teacher_compare(db, course_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trend/teacher")
def api_teacher_trend(course_id: int, db: Session = Depends(get_db),
                      user: dict = Depends(get_current_user)):
    try:
        return teacher_trend(db, course_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
