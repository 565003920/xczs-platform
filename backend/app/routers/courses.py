from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.routers.auth import get_current_user
from app.models.teaching import Course
from app.schemas.teaching import CourseCreate, CourseResponse, CourseDetail

router = APIRouter(prefix="/api/courses", tags=["courses"])


def _owner_filter(q, user: dict):
    if user.get("role") != "admin":
        q = q.filter((Course.owner_id == user["user_id"]) | (Course.owner_id == None))
    return q


@router.get("", response_model=List[CourseResponse])
def list_courses(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return _owner_filter(db.query(Course), user).all()


@router.get("/{course_id}", response_model=CourseDetail)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course: raise HTTPException(404, "课程不存在")
    return course


@router.post("", response_model=CourseResponse)
def create_course(data: CourseCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    course = Course(**data.model_dump(), owner_id=user["user_id"])
    db.add(course); db.commit(); db.refresh(course)
    return course
