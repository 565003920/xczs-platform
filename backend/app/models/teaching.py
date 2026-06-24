from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="课程名称")
    code = Column(String(50), unique=True, nullable=False, comment="课程代码")
    department = Column(String(100), comment="开课院系")
    credits = Column(Float, default=3.0, comment="学分")
    teacher_name = Column(String(100), comment="授课教师")
    semester = Column(String(50), comment="学期，如 2024-2025-1")
    created_at = Column(DateTime, server_default=func.now())

    classes = relationship("ClassModel", back_populates="course", cascade="all, delete-orphan")


class ClassModel(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="班级名称")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    semester = Column(String(50), comment="学期")
    student_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

    course = relationship("Course", back_populates="classes")
    students = relationship("Student", back_populates="class_", cascade="all, delete-orphan")
    observations = relationship("Observation", back_populates="class_", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="class_", cascade="all, delete-orphan")
    grades = relationship("Grade", back_populates="class_", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    student_no = Column(String(50), unique=True, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    class_ = relationship("ClassModel", back_populates="students")
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")


class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    date = Column(String(50), comment="观察日期")
    observer = Column(String(100), comment="观察者")
    interaction_frequency = Column(Integer, default=3, comment="互动频次 1-5")
    question_depth = Column(Integer, default=3, comment="提问深度 1-5")
    student_participation = Column(Integer, default=3, comment="学生参与度 1-5")
    lecture_ratio = Column(Float, default=0.5, comment="讲授占比")
    discussion_ratio = Column(Float, default=0.3, comment="讨论占比")
    practice_ratio = Column(Float, default=0.2, comment="实践占比")
    teaching_style_label = Column(String(100), comment="教学模式标签")
    notes = Column(String(500), comment="备注")
    created_at = Column(DateTime, server_default=func.now())

    class_ = relationship("ClassModel", back_populates="observations")


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    exam_name = Column(String(200), comment="考试名称")
    score = Column(Float, nullable=False)
    knowledge_point = Column(String(200), comment="知识点")
    max_score = Column(Float, default=100.0)
    created_at = Column(DateTime, server_default=func.now())

    student = relationship("Student", back_populates="grades")
    class_ = relationship("ClassModel", back_populates="grades")


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    semester = Column(String(50))
    dimension = Column(String(100), comment="评价维度")
    score = Column(Float, nullable=False, comment="评分")
    created_at = Column(DateTime, server_default=func.now())

    class_ = relationship("ClassModel", back_populates="evaluations")
