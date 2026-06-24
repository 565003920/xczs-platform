from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ---- Course ----
class CourseCreate(BaseModel):
    name: str
    code: str
    department: Optional[str] = ""
    credits: float = 3.0
    teacher_name: Optional[str] = ""
    semester: Optional[str] = ""


class CourseResponse(BaseModel):
    id: int
    name: str
    code: str
    department: Optional[str]
    credits: float
    teacher_name: Optional[str]
    semester: Optional[str]

    model_config = {"from_attributes": True}


class CourseDetail(CourseResponse):
    classes: List["ClassResponse"] = []

    model_config = {"from_attributes": True}


# ---- Class ----
class ClassCreate(BaseModel):
    name: str
    course_id: int
    semester: Optional[str] = ""
    student_count: int = 0


class ClassResponse(BaseModel):
    id: int
    name: str
    course_id: int
    semester: Optional[str]
    student_count: int

    model_config = {"from_attributes": True}


class ClassDetail(ClassResponse):
    course: Optional[CourseResponse] = None
    students: List["StudentResponse"] = []

    model_config = {"from_attributes": True}


# ---- Student ----
class StudentCreate(BaseModel):
    name: str
    student_no: str
    class_id: int


class StudentResponse(BaseModel):
    id: int
    name: str
    student_no: str
    class_id: int

    model_config = {"from_attributes": True}


# ---- Grade ----
class GradeCreate(BaseModel):
    student_id: int
    class_id: int
    exam_name: str
    score: float
    knowledge_point: Optional[str] = ""
    max_score: float = 100.0


class GradeResponse(BaseModel):
    id: int
    student_id: int
    class_id: int
    exam_name: str
    score: float
    knowledge_point: Optional[str]
    max_score: float

    model_config = {"from_attributes": True}


# ---- Observation ----
class ObservationCreate(BaseModel):
    class_id: int
    date: Optional[str] = ""
    observer: Optional[str] = ""
    interaction_frequency: int = 3
    question_depth: int = 3
    student_participation: int = 3
    lecture_ratio: float = 0.5
    discussion_ratio: float = 0.3
    practice_ratio: float = 0.2
    teaching_style_label: Optional[str] = ""
    notes: Optional[str] = ""


class ObservationResponse(BaseModel):
    id: int
    class_id: int
    date: Optional[str]
    observer: Optional[str]
    interaction_frequency: int
    question_depth: int
    student_participation: int
    lecture_ratio: float
    discussion_ratio: float
    practice_ratio: float
    teaching_style_label: Optional[str]
    notes: Optional[str]

    model_config = {"from_attributes": True}


# ---- Evaluation ----
class EvaluationCreate(BaseModel):
    class_id: int
    semester: Optional[str] = ""
    dimension: str
    score: float


class EvaluationResponse(BaseModel):
    id: int
    class_id: int
    semester: Optional[str]
    dimension: str
    score: float

    model_config = {"from_attributes": True}


# ---- Import Result ----
class ImportResult(BaseModel):
    imported: int
    errors: List[str] = []


# ---- Analysis: Profile ----
class DimensionScores(BaseModel):
    knowledge_mastery: float = 0.0
    participation: float = 0.0
    interaction_quality: float = 0.0
    question_depth: float = 0.0
    practice_balance: float = 0.0
    satisfaction: float = 0.0


class KnowledgePoint(BaseModel):
    knowledge_point: str
    avg_score: float


class ClassProfileResponse(BaseModel):
    class_id: int
    class_name: str
    course_name: str
    dimensions: DimensionScores
    weak_points: List[KnowledgePoint] = []
    strengths: List[KnowledgePoint] = []
    student_count: int = 0
    avg_grade: float = 0.0
    grade_distribution: dict = {}


# ---- Analysis: Fingerprint ----
class FingerprintScores(BaseModel):
    lecture_oriented: float = 0.0
    interactive: float = 0.0
    practice_oriented: float = 0.0
    question_level: float = 0.0
    student_centeredness: float = 0.0


class ModeFingerprintResponse(BaseModel):
    class_id: int
    fingerprint: FingerprintScores
    mode_label: str = ""
    mode_description: str = ""
    mode_recommendations: List[str] = []
    observation_count: int = 0


# ---- Analysis: Diagnosis ----
class DiagnosisResponse(BaseModel):
    class_id: int
    class_name: str
    course_name: str
    profile: ClassProfileResponse
    fingerprint: ModeFingerprintResponse
    teaching_mode_suggestion: str = ""
