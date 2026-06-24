from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.teaching import Course
from app.schemas.teaching import CourseCreate, CourseResponse, CourseDetail

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("", response_model=List[CourseResponse])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


@router.get("/{course_id}", response_model=CourseDetail)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course


@router.post("", response_model=CourseResponse)
def create_course(data: CourseCreate, db: Session = Depends(get_db)):
    course = Course(**data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
