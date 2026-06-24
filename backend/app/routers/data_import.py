from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import pandas as pd
import io
from typing import List

from app.database import get_db
from app.models.teaching import Course, ClassModel, Student, Grade, Observation, Evaluation
from app.schemas.teaching import ImportResult

router = APIRouter(prefix="/api/import", tags=["data_import"])


def _parse_csv(file: UploadFile) -> pd.DataFrame:
    content = file.file.read()
    return pd.read_csv(io.BytesIO(content))


@router.post("/courses", response_model=ImportResult)
async def import_courses(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = _parse_csv(file)
        count = 0
        for _, row in df.iterrows():
            existing = db.query(Course).filter(Course.code == str(row.get("code", ""))).first()
            if existing:
                continue
            db.add(Course(
                name=str(row.get("name", "")),
                code=str(row.get("code", "")),
                department=str(row.get("department", "")),
                credits=float(row.get("credits", 3.0)),
                teacher_name=str(row.get("teacher_name", "")),
                semester=str(row.get("semester", "")),
            ))
            count += 1
        db.commit()
        return ImportResult(imported=count)
    except Exception as e:
        return ImportResult(imported=0, errors=[str(e)])


@router.post("/classes", response_model=ImportResult)
async def import_classes(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = _parse_csv(file)
        count = 0
        for _, row in df.iterrows():
            db.add(ClassModel(
                name=str(row.get("name", "")),
                course_id=int(row.get("course_id", 0)),
                semester=str(row.get("semester", "")),
                student_count=int(row.get("student_count", 0)),
            ))
            count += 1
        db.commit()
        return ImportResult(imported=count)
    except Exception as e:
        return ImportResult(imported=0, errors=[str(e)])


@router.post("/students", response_model=ImportResult)
async def import_students(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = _parse_csv(file)
        count = 0
        for _, row in df.iterrows():
            existing = db.query(Student).filter(Student.student_no == str(row.get("student_no", ""))).first()
            if existing:
                continue
            db.add(Student(
                name=str(row.get("name", "")),
                student_no=str(row.get("student_no", "")),
                class_id=int(row.get("class_id", 0)),
            ))
            count += 1
        db.commit()
        return ImportResult(imported=count)
    except Exception as e:
        return ImportResult(imported=0, errors=[str(e)])


@router.post("/grades", response_model=ImportResult)
async def import_grades(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = _parse_csv(file)
        count = 0
        for _, row in df.iterrows():
            db.add(Grade(
                student_id=int(row.get("student_id", 0)),
                class_id=int(row.get("class_id", 0)),
                exam_name=str(row.get("exam_name", "")),
                score=float(row.get("score", 0)),
                knowledge_point=str(row.get("knowledge_point", "")),
                max_score=float(row.get("max_score", 100.0)),
            ))
            count += 1
        db.commit()
        return ImportResult(imported=count)
    except Exception as e:
        return ImportResult(imported=0, errors=[str(e)])


@router.post("/observations", response_model=ImportResult)
async def import_observations(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = _parse_csv(file)
        count = 0
        for _, row in df.iterrows():
            db.add(Observation(
                class_id=int(row.get("class_id", 0)),
                date=str(row.get("date", "")),
                observer=str(row.get("observer", "")),
                interaction_frequency=int(row.get("interaction_frequency", 3)),
                question_depth=int(row.get("question_depth", 3)),
                student_participation=int(row.get("student_participation", 3)),
                lecture_ratio=float(row.get("lecture_ratio", 0.5)),
                discussion_ratio=float(row.get("discussion_ratio", 0.3)),
                practice_ratio=float(row.get("practice_ratio", 0.2)),
                teaching_style_label=str(row.get("teaching_style_label", "")),
                notes=str(row.get("notes", "")),
            ))
            count += 1
        db.commit()
        return ImportResult(imported=count)
    except Exception as e:
        return ImportResult(imported=0, errors=[str(e)])


@router.post("/evaluations", response_model=ImportResult)
async def import_evaluations(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = _parse_csv(file)
        count = 0
        for _, row in df.iterrows():
            db.add(Evaluation(
                class_id=int(row.get("class_id", 0)),
                semester=str(row.get("semester", "")),
                dimension=str(row.get("dimension", "")),
                score=float(row.get("score", 0)),
            ))
            count += 1
        db.commit()
        return ImportResult(imported=count)
    except Exception as e:
        return ImportResult(imported=0, errors=[str(e)])
