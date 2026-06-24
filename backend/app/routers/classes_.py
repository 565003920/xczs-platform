from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.database import get_db
from app.routers.auth import get_current_user, filter_classes_by_owner
from app.models.teaching import ClassModel
from app.schemas.teaching import ClassCreate, ClassResponse, ClassDetail

router = APIRouter(prefix="/api/classes", tags=["classes"])


@router.get("", response_model=List[ClassResponse])
def list_classes(course_id: Optional[int] = None, db: Session = Depends(get_db),
                 user: dict = Depends(get_current_user)):
    q = db.query(ClassModel)
    if course_id:
        q = q.filter(ClassModel.course_id == course_id)
    return filter_classes_by_owner(q, user).all()


@router.get("/{class_id}", response_model=ClassDetail)
def get_class(class_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    cls = db.query(ClassModel).filter(ClassModel.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail="班级不存在")
    return cls


@router.post("", response_model=ClassResponse)
def create_class(data: ClassCreate, db: Session = Depends(get_db)):
    cls = ClassModel(**data.model_dump())
    db.add(cls); db.commit(); db.refresh(cls)
    return cls
