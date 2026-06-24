"""Seed demo data into the SQLite database."""
import sys
import os
import pandas as pd
from sqlalchemy.orm import Session

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine, SessionLocal, Base
from app.models.teaching import Course, ClassModel, Student, Grade, Observation, Evaluation

DATA_DIR = os.path.join(os.path.dirname(__file__), "sample_data")


def import_csv(db: Session, model, filepath: str, field_map: dict):
    df = pd.read_csv(filepath)
    count = 0
    for _, row in df.iterrows():
        kwargs = {}
        for csv_col, db_col in field_map.items():
            kwargs[db_col] = row[csv_col]
        db.add(model(**kwargs))
        count += 1
    db.commit()
    print(f"  Imported {count} rows into {model.__tablename__}")


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(Course).count() > 0:
            print("Database already has data. Skipping seed.")
            return

        print("Seeding database...")

        import_csv(db, Course, os.path.join(DATA_DIR, "courses.csv"), {
            "name": "name", "code": "code", "department": "department",
            "credits": "credits", "teacher_name": "teacher_name", "semester": "semester",
        })

        import_csv(db, ClassModel, os.path.join(DATA_DIR, "classes.csv"), {
            "name": "name", "course_id": "course_id", "semester": "semester",
            "student_count": "student_count",
        })

        import_csv(db, Student, os.path.join(DATA_DIR, "students.csv"), {
            "name": "name", "student_no": "student_no", "class_id": "class_id",
        })

        import_csv(db, Grade, os.path.join(DATA_DIR, "grades.csv"), {
            "student_id": "student_id", "class_id": "class_id", "exam_name": "exam_name",
            "score": "score", "knowledge_point": "knowledge_point", "max_score": "max_score",
        })

        import_csv(db, Observation, os.path.join(DATA_DIR, "observations.csv"), {
            "class_id": "class_id", "date": "date", "observer": "observer",
            "interaction_frequency": "interaction_frequency", "question_depth": "question_depth",
            "student_participation": "student_participation", "lecture_ratio": "lecture_ratio",
            "discussion_ratio": "discussion_ratio", "practice_ratio": "practice_ratio",
            "teaching_style_label": "teaching_style_label", "notes": "notes",
        })

        import_csv(db, Evaluation, os.path.join(DATA_DIR, "evaluations.csv"), {
            "class_id": "class_id", "semester": "semester", "dimension": "dimension",
            "score": "score",
        })

        print("Seeding complete!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
