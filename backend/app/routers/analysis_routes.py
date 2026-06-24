from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.analysis import get_class_profile, get_mode_fingerprint, get_diagnosis
from app.schemas.teaching import ClassProfileResponse, ModeFingerprintResponse, DiagnosisResponse

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.get("/profile/{class_id}", response_model=ClassProfileResponse)
def class_profile(class_id: int, db: Session = Depends(get_db)):
    try:
        return get_class_profile(db, class_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/fingerprint/{class_id}", response_model=ModeFingerprintResponse)
def class_fingerprint(class_id: int, db: Session = Depends(get_db)):
    try:
        return get_mode_fingerprint(db, class_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/diagnosis/{class_id}", response_model=DiagnosisResponse)
def class_diagnosis(class_id: int, db: Session = Depends(get_db)):
    try:
        return get_diagnosis(db, class_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
